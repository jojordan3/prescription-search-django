from django.shortcuts import render
from . import forms
from .models import RxClaim, PharmacyInfo, BrandToGeneric, ZipCodeInfo
import pandas as pd
from . import search_functions as sf


def home(request):
    '''renders the home page
    '''
    return render(request, 'rx_info/Med_Dashboard_Story.html', {})


def pharmacy_info(request):
    '''renders the local pharmacy search page
    '''
    form = forms.pharmacyForm()
    return render(request, 'rx_info/pharmacy_info.html', {"form": form})


def PBM_info(request):
    '''renders the PBM search page
    '''
    return render(request, 'rx_info/PBM_info.html', {})


def pharmacy_results(request):
    '''renders the pharmacy search results
    '''
    # Get the input from the form from the pharmacy_info page
    zipcode = request.GET.get('zip_code')
    drug = request.GET.get('drug')
    quantity = request.GET.get('quantity')

    # force the characters in the drug string to upper case to match database
    # Define variables from the input zip code and drug name to match the
    # two engineered columns
    drug = drug.lower()
    # Make sure quantity is read as an integer
    quantity = int(quantity)
    try:
        df = sf.search_by_pharm(drug, zipcode)
        df['EstimatedPrice'] = df.UnitCost.apply(lambda x:
                                                 f'${(quantity * x):.2f}')
        ph_df = sf.get_pharm_info(df.index.values.tolist())
        results = pd.concat([ph_df, df], axis=1, ignore_index=True)
        results = results.drop(columns=['UnitCost'])

        # Convert df to html
        data_html = results.to_html(index=False)
        context = {'loaded_data': data_html}
        return render(request, 'rx_info/pharmacy_results.html', context)
    except:
        return render(request, 'rx_info/no_pharmacy_results.html', {})


def PBM_results(request):
    '''renders PBM search results page
    '''
    # Get the input from the form from the pharmacy_info page
    drug = request.GET.get('drug')
    # force the characters in the drug string to upper case to match database
    drug = drug.lower()

    try:
        df = sf.search_by_pbm(drug)
        data_html = sorted_pbms.to_html(index=False)

        # Convert results to html
        context = {'loaded_data': data_html}
        return render(request, 'rx_info/PBM_results.html', context)
    except:
        return render(request, 'rx_info/no_PBM_results.html', {})
