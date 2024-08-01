from django.shortcuts import get_object_or_404, redirect, render
from .models import Inventoryandy
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm
from django.contrib import messages
from django_pandas.io import  read_frame
import pandas as pd
import plotly
import plotly.express as px
import json
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def inventoryandy_list(request):
    inventories = Inventoryandy.objects.all()
    for inventory in inventories:
        inventory.sales_or_revenue = inventory.quantity_sold * inventory.cost_per_item
        inventory.remaining_quantity = inventory.quantity_in_stock - inventory.quantity_sold
    context ={
        "title": "Inventoryandy List",
        "inventories": inventories
    }
    return render(request, 'inventoryandy/inventoryandy_list.html', context=context)


@login_required
def per_product_view(request, pk):
    inventoryandy = get_object_or_404(Inventoryandy, pk=pk)
    context = {
        'inventoryandy': inventoryandy
    }
    
    return render(request, "inventoryandy/per_product.html", context=context)

@login_required
def add_product(request):
    if request.method == 'POST':
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventoryandy =add_form.save(commit=False)
            new_inventoryandy.sales_or_revenue = float (add_form.data['cost_per_item']) * float(add_form.data['quantity_sold'])
            new_inventoryandy.remaining_quantity = float (add_form.data['quantity_in_stock']) - float(add_form.data['quantity_sold'])
            new_inventoryandy.save()
            messages.success(request, "Successfully Added Product")
        return redirect("inventoryandy_list") 
    else:
        add_form = AddInventoryForm()
    return render (request, "inventoryandy/inventory_add.html",{"form": add_form})

@login_required
def delete_inventory(request, pk):
    inventoryandy = get_object_or_404(Inventoryandy, pk=pk)
    inventoryandy.delete()
    messages.success(request, "Successfully deleted Product")
    return redirect("/inventoryandy/")


@login_required
def update_inventory(request, pk):
    inventoryandy = get_object_or_404(Inventoryandy, pk=pk)
    if request.method == "POST":
        updateForm = UpdateInventoryForm(request.POST, instance=inventoryandy)
        if updateForm.is_valid():
            updateForm.save()
            inventoryandy.sales = float(inventoryandy.cost_per_item) * float(inventoryandy.quantity_sold)
            inventoryandy.save()
            messages.success(request, "Product Succesfully Updated")
            return redirect("/inventoryandy/")
    else:
        updateForm = UpdateInventoryForm(instance=inventoryandy)
    context = {"form": updateForm}
    return render(request, "inventoryandy/inventory_update.html", context)

@login_required
def dashboard(request):
    inventories = Inventoryandy.objects.all()
    
    df = read_frame(inventories)
    
    df['last_sales_date'] = pd.to_datetime(df['last_sales_date'])
    
    sales_graph = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
    sales_graph = px.line(sales_graph, x="last_sales_date", y="sales", title="ANDY Sales Trend")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)
    
    numeric_columns = ['quantity_sold', 'sales']
    best_performing_product_df = df.groupby(by="name")[numeric_columns].sum().sort_values(by="quantity_sold")
    best_performing_product = px.bar(best_performing_product_df, x = best_performing_product_df.index, y = best_performing_product_df.quantity_sold, title = "Andy's Best Performing Product")
    best_performing_product = json.dumps(best_performing_product, cls = plotly.utils.PlotlyJSONEncoder)
    
    numeric_columns = ['quantity_sold', 'sales',]
    best_income_generating_product_df = df.groupby(by="name")[numeric_columns].sum().sort_values(by="sales")
    best_income_generating_product = px.bar(best_income_generating_product_df, x = best_income_generating_product_df.index, y = best_income_generating_product_df.sales, title = "Andy's Best Income Generating Product")
    best_income_generating_product = json.dumps(best_income_generating_product, cls = plotly.utils.PlotlyJSONEncoder)
    
    numeric_columns = ['quantity_sold', 'sales', 'quantity_in_stock']
    most_product_in_stock_df = df.groupby(by="name")[numeric_columns].sum().sort_values(by="quantity_in_stock")
    most_product_in_stock =px.pie(most_product_in_stock_df, names = most_product_in_stock_df.index, values = most_product_in_stock_df.quantity_in_stock, title = " Andy's intial Most Product in Stock")
    most_product_in_stock = json.dumps(most_product_in_stock, cls = plotly.utils.PlotlyJSONEncoder)
    
    numeric_columns = ['remaining_quantity']
    current_product_in_stock_df = df.groupby(by="name")[numeric_columns].sum().sort_values(by="remaining_quantity")
    current_product_in_stock = px.pie(current_product_in_stock_df, names = current_product_in_stock_df.index, values = current_product_in_stock_df.remaining_quantity, title="Andy's Current Product in Stock")
    current_product_in_stock = json.dumps(current_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)
    
    context = { 
            "sales_graph": sales_graph,
            "best_performing_product" : best_performing_product,
            "best_income_generating_product" : best_income_generating_product,
            "most_product_in_stock" : most_product_in_stock,
            "current_product_in_stock" : current_product_in_stock
    }
    
    return render(request, "inventoryandy/dashboard.html", context=context)


@login_required
def handle_scan(request):
    if request.method == 'POST':
        scanned_data = request.POST.get('scanned_data')
        # Assuming 'scanned_data' contains the barcode value
        # Query the Inventoryandy model to find the corresponding product
        inventoryandy = Inventoryandy.objects.filter(barcode=scanned_data).first()
        if inventoryandy:
            # If the product is found, redirect to its update page
            return HttpResponseRedirect(reverse('update_inventory', args=[inventoryandy.pk]))
        else:
            # If the product is not found, return an error response
            return JsonResponse({'error': 'Product not found for the scanned barcode'}, status=404)
    else:
        # Return a method not allowed response for non-POST requests
        return JsonResponse({'error': 'Method not allowed'}, status=405)