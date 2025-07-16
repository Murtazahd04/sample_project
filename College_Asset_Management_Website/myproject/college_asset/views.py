from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisteredAssetForm, ClassroomForm, ClassroomAssetForm
from .models import RegisteredAsset, Classroom, ClassroomAsset
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.auth.decorators import login_required


def register_asset(request):
    if request.method == 'POST':
        form = RegisteredAssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('college_asset:classroom_list')  # Updated with namespace
    else:
        form = RegisteredAssetForm()
    return render(request, 'classroom/register_asset.html', {'form': form})

def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('college_asset:classroom_list')  # Updated with namespace
    else:
        form = ClassroomForm()
    return render(request, 'classroom/add_classroom.html', {'form': form})

# Similarly, update all other redirect calls in views.py

def assign_asset(request):
    if request.method == 'POST':
        form = ClassroomAssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('college_asset:classroom_list') # Replace with your list view name
    else:
        form = ClassroomAssetForm()
    return render(request, 'classroom/assign_asset.html', {'form': form})

def classroom_list(request):
    classrooms = Classroom.objects.all()
    classroom_assets = ClassroomAsset.objects.all()
    registered_assets = RegisteredAsset.objects.all()
    return render(request, 'classroom/classroom_list.html', {'classrooms': classrooms, 'classroom_assets': classroom_assets, 'registered_assets': registered_assets})

def edit_asset(request, asset_id):
    asset = get_object_or_404(RegisteredAsset, pk=asset_id)
    if request.method == 'POST':
        form = RegisteredAssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('college_asset:classroom_list')  # Replace with your list view name
    else:
        form = RegisteredAssetForm(instance=asset)
    return render(request, 'classroom/edit_asset.html', {'form': form, 'asset': asset})

def edit_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('college_asset:classroom_list')
    else:
        form = ClassroomForm(instance=classroom)
    return render(request, 'classroom/edit_classroom.html', {'form': form, 'classroom': classroom})

def edit_classroom_asset(request, classroom_asset_id):
    classroom_asset = get_object_or_404(ClassroomAsset, pk=classroom_asset_id)
    if request.method == 'POST':
        form = ClassroomAssetForm(request.POST, instance=classroom_asset)
        if form.is_valid():
            form.save()
            return redirect('college_asset:classroom_list')
    else:
        form = ClassroomAssetForm(instance=classroom_asset)
    return render(request, 'classroom/edit_classroom_asset.html', {'form': form, 'classroom_asset': classroom_asset})

def delete_asset(request, asset_id):
    asset = get_object_or_404(RegisteredAsset, pk=asset_id)
    if request.method == 'POST':
        asset.delete()
        return redirect('college_asset:classroom_list')
    return render(request, 'classroom/delete_asset.html', {'asset': asset})

def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if request.method == 'POST':
        classroom.delete()
        return redirect('college_asset:classroom_list')
    return render(request, 'classroom/delete_classroom.html', {'classroom': classroom})

def delete_classroom_asset(request, classroom_asset_id):
    classroom_asset = get_object_or_404(ClassroomAsset, pk=classroom_asset_id)
    if request.method == 'POST':
        classroom_asset.delete()
        return redirect('college_asset:classroom_list')
    return render(request, 'classroom/delete_classroom_asset.html', {'classroom_asset': classroom_asset})

def classroom_report(request):
    classrooms = Classroom.objects.all()
    selected_classroom = None
    classroom_assets = []

    # Check if a classroom is selected
    if request.method == 'GET' and 'classroom_id' in request.GET:
        classroom_id = request.GET.get('classroom_id')
        selected_classroom = Classroom.objects.get(pk=classroom_id)
        classroom_assets = ClassroomAsset.objects.filter(classroom=selected_classroom)

    return render(request, 'classroom/classroom_report.html', {
        'classrooms': classrooms,
        'selected_classroom': selected_classroom,
        'classroom_assets': classroom_assets,
    })

def asset_pie_chart(request):
    # Fetch all registered assets
    registered_assets = RegisteredAsset.objects.all()

    # Prepare data for each asset
    asset_charts = []
    for asset in registered_assets:
        # Fetch all classroom assets related to this registered asset
        classroom_assets = ClassroomAsset.objects.filter(asset=asset)

        # Calculate total quantities and inactive quantities for this asset
        total_quantity = sum(int(ca.quantity or 0) for ca in classroom_assets)
        total_inactive_quantity = sum(int(ca.inactive_quantity or 0) for ca in classroom_assets)

        # Skip if there is no data for this asset
        if total_quantity == 0:
            continue

        # Data for the pie chart
        labels = ['Active Quantity', 'Inactive Quantity']
        sizes = [total_quantity - total_inactive_quantity, total_inactive_quantity]
        colors = ['#44B78B', '#FF6F61']  # Colors for the pie chart
        explode = (0.1, 0)  # Explode the inactive quantity slice for emphasis

        # Generate the pie chart
        plt.figure(figsize=(6, 4))
        plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)
        plt.title(f'{asset.asset_name} Quantity vs Inactive Quantity')
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

        # Save the chart to a BytesIO buffer and encode it as Base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()

        # Get classrooms where the asset is inactive
        inactive_classrooms = classroom_assets.filter(inactive_quantity__gt=0).values(
            'classroom__classroom_no', 'classroom__division', 'inactive_quantity'
        )

        # Append the chart data and inactive classroom details to the list
        asset_charts.append({
            'asset_name': asset.asset_name,
            'chart': image_base64,
            'inactive_classrooms': inactive_classrooms
        })

    # Pass the list of charts to the template
    return render(request, 'classroom/asset_pie_chart.html', {'asset_charts': asset_charts})