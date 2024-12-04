from django.shortcuts import render
import pandas as pd
import pickle


# Create your views here.
def index(request):
    if request.method == 'POST':
        classification_mapping = {0.0:'AMO', 1.0 :'MBA', 2.0:'MCA', 3.0:'APO', 4.0:'IMB', 5.0:'OMB'}
        form_type = request.POST.get('form_type')
        if form_type == 'csv':
            dataset = request.FILES.get('dataset_file')
            astro_df = pd.read_csv(dataset, delimiter='\t')
            X = astro_df[["perihelion_point", "aphelion_point"]]
            with open ('Classification/static/trained_model/trained_model_knn.sav', 'rb') as file:
                knn_model = pickle.load(file)
            y = knn_model.predict(X)
            
            astro_df["classification_numerical"] = y
            X["classification_numerical"] = y
            X["classification"] = X["classification_numerical"].map(classification_mapping)
            astro_df["classification"] = astro_df["classification_numerical"].map(classification_mapping)

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
            return render(request, 'classification/output.html', context)
        else:
            perihelion = request.POST.get('perihelion')
            aphelion = request.POST.get('aphelion')
            astro_df = pd.DataFrame()
            astro_df['perihelion_point'] = [perihelion]
            astro_df['aphelion_point'] = [aphelion]

            with open ('Classification/static/trained_model/trained_model_knn.sav', 'rb') as file:
                knn_model = pickle.load(file)
            y = knn_model.predict(astro_df)
            astro_df["classification_numerical"] = y
            astro_df["classification"] = astro_df["classification_numerical"].map(classification_mapping)

            reduced_columns = astro_df.columns.tolist()
            reduced_data = astro_df.values.tolist()

            context = {
                'mode': 'single',
                'columns': reduced_columns,
                'data': reduced_data,
                'all_columns': reduced_columns,
                'all_data': reduced_data,
            }

            return render(request, 'classification/output.html', context)
    
    # When its a GET request, form not sent
    return render(request, 'classification/input.html')
