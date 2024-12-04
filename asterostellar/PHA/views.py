from django.shortcuts import render
import pickle
import pandas as pd
# Create your views here.

def index(request):
    if request.method == 'POST':
        pha_flag_mapping = {0: 'Not Hazardous', 1: 'Potentially Hazardous'}
        form_type = request.POST.get('form_type')
        print(form_type)
        if form_type == 'csv':
            dataset = request.FILES.get('dataset_file')
            astro_df = pd.read_csv(dataset, delimiter='\t')
            X = astro_df[["absolute_magnitude", "semi_major_axis", "perihelion_point", "mean_motion"]]
            with open ('PHA/static/trained_models/trained_model_dt.sav', 'rb') as file:
                dt_model = pickle.load(file)
            y = dt_model.predict(X)
            
            X["pha_flag_numerical"] = y
            astro_df["pha_flag_numerical"] = y

            X["pha_flag"] = X["pha_flag_numerical"].map(pha_flag_mapping)
            astro_df["pha_flag"] = astro_df["pha_flag_numerical"].map(pha_flag_mapping)

            reduced_columns = X.columns.tolist()
            reduced_data = X.values.tolist()
            astro_df_columns = astro_df.columns.tolist()
            astro_df_data = astro_df.values.tolist()
            
            print(y)

            context = {
                'mode': 'csv',
                'columns': reduced_columns,
                'data': reduced_data,
                'all_columns': astro_df_columns,
                'all_data': astro_df_data,
            }
            return render(request, 'pha/output.html', context)
        else:
            absolute_magnitude = request.POST.get('absolute_magnitude')
            semi_major_axis = request.POST.get('semi_major_axis')
            perihelion_point = request.POST.get('perihelion_point')
            mean_motion = request.POST.get('mean_motion')

            astro_df = pd.DataFrame()
            astro_df['absolute_magnitude'] = [absolute_magnitude]
            astro_df['semi_major_axis'] = [semi_major_axis]
            astro_df['perihelion_point'] = [perihelion_point]
            astro_df['mean_motion'] = [mean_motion]

            with open ('PHA/static/trained_models/trained_model_dt.sav', 'rb') as file:
                dt_model = pickle.load(file)
            y = dt_model.predict(astro_df)

            astro_df["pha_flag_numerical"] = y
            astro_df["pha_flag"] = astro_df["pha_flag_numerical"].map(pha_flag_mapping)

            reduced_columns = astro_df.columns.tolist()
            reduced_data = astro_df.values.tolist()

            context = {
                'mode': 'single',
                'columns': reduced_columns,
                'data': reduced_data,
                'all_columns': reduced_columns,
                'all_data': reduced_data,
            }
            return render(request, 'pha/output.html', context)

    
    # When its a GET request, form not sent
    return render(request, 'pha/input.html')
    