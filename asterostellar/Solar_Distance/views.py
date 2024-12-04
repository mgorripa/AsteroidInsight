from django.shortcuts import render
import pandas as pd
import pickle


# Create your views here.
def index(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'csv':
            dataset = request.FILES.get('dataset_file')
            astro_df = pd.read_csv(dataset, delimiter='\t')
            X = astro_df[["semi_major_axis", "eccentricity"]]
            with open ('Solar_Distance/static/trained_models/trained_model_linear_regression.sav', 'rb') as file:
                linear_model = pickle.load(file)
            y = linear_model.predict(X)
            X['perihelion_distance'] = y
            reduced_columns = X.columns.tolist()
            reduced_data = X.values.tolist()
            astro_df_columns = astro_df.columns.tolist()
            astro_df_data = astro_df.values.tolist()
                
            context = {
                'mode': 'csv',
                'columns': reduced_columns,
                'data': reduced_data,
                'all_columns': astro_df_columns,
                'all_data': astro_df_data,
            }
            return render(request, 'solar_distance/output.html', context)
        else:
            semi_major_axis = request.POST.get('semi_major_axis')
            eccentricity = request.POST.get('eccentricity')

            astro_df = pd.DataFrame()
            astro_df['semi_major_axis'] = [semi_major_axis]
            astro_df['eccentricity'] = [eccentricity]

            with open ('Solar_Distance/static/trained_models/trained_model_linear_regression.sav', 'rb') as file:
                linear_model = pickle.load(file)
            y = linear_model.predict(astro_df)

            astro_df["perihelion_distance"] = y

            reduced_columns = astro_df.columns.tolist()
            reduced_data = astro_df.values.tolist()

            context = {
                'mode': 'single',
                'columns': reduced_columns,
                'data': reduced_data,
                'all_columns': reduced_columns,
                'all_data': reduced_data,
            }
            return render(request, 'solar_distance/output.html', context)
                
    # When its a GET request, form not sent
    return render(request, 'solar_distance/input.html')
