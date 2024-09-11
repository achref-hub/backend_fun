import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate


# Read the data from CSV file
df = pd.read_csv('./data/sheet.csv')

df.columns = df.columns.map(lambda x: x.capitalize())
# Liste des colonnes à conserver
colonnes_a_garder = ["Colis", "Nom destinataire","Tel 1", "Tel 2", "Genre", "Gouvernorat", "Description", "Statut", "Date de création", "Cr apres remise"]
# Supprimer les colonnes autres que celles à conserver
colonnes_a_supprimer = [colonne for colonne in df.columns if colonne not in colonnes_a_garder]
df = df.drop(columns=colonnes_a_supprimer)
# Renommer la colonne "Date de création" en "Date"
df.rename(columns={"Date de création": "Date"}, inplace=True)
# Remplacer les valeurs "h" ou "H" par "Homme" et les valeurs "f" ou "F" par "Femme" dans la colonne "Statut"
df['Genre'] = df['Genre'].replace({'h': 'Homme', 'H': 'Homme', 'f': 'Femme', 'F': 'Femme'})
# Remplacer les valeurs dans la colonne "Statut"
df["Statut"] = df["Statut"].replace({
    "Annulé": "Retour",
    "Reçu par l'expediteur": "Retour",
    "En cours de préparation au retour vers l'expéditeur": "Retour",
    "En attente": "Non confirmé",
    "à enlever": "Non confirmé",
    "En cours de livraison": "Non confirmé",
    "En cours de préparation au transfert vers une autre agence": "Non confirmé",
    "En cours de prépartion à l'expédition": "Non confirmé",
    "Reçu à l'entrepôt": "Non confirmé",
    "Transfert a une autre agence en cours": "Non confirmé",
})

# Convertir le DataFrame en tableau
table = tabulate(df, headers='keys', tablefmt='pretty')
# Regroupement par gouvernorat et calcul de la Somme_de_Cr_apres_remise par gouvernorat
sum_by_gouvernorat = df.groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_by_gouvernorat = sum_by_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise'})

# Regroupement par gouvernorat et comptage du Nombre_total_de_colis par gouvernorat
count_by_gouvernorat = df.groupby('Gouvernorat')['Colis'].count().reset_index()
count_by_gouvernorat = count_by_gouvernorat.rename(columns={'Colis': 'Nombre_total_de_colis'})

# Fusionner les DataFrames sum_by_gouvernorat et count_by_gouvernorat sur la colonne Gouvernorat
result = pd.merge(sum_by_gouvernorat, count_by_gouvernorat, on='Gouvernorat')

# Filtrer les lignes où le statut est "Livré" et compter le Nombre_de_Colis_Livrés par gouvernorat
colis_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_livres_par_gouvernorat = colis_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Livrés'})

# Ajouter une colonne avec le Nombre_de_Colis_Livrés par gouvernorat
result = pd.merge(result, colis_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Livré" et calculer la Somme_de_Cr_apres_remise_des_colis_livrés par gouvernorat
sum_cr_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_livres_par_gouvernorat = sum_cr_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et compter le Nombre_de_Colis_Retournés par gouvernorat
colis_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_retournes_par_gouvernorat = colis_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Retournés'})

# Ajouter une colonne avec le Nombre_de_Colis_Retournés par gouvernorat
result = pd.merge(result, colis_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et calculer la Somme_de_Cr_apres_remise_des_colis_retournés par gouvernorat
sum_cr_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_retournes_par_gouvernorat = sum_cr_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Regroupement par gouvernorat et calcul de la Somme_de_Cr_apres_remise par gouvernorat
sum_by_gouvernorat = df.groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_by_gouvernorat = sum_by_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise'})

# Regroupement par gouvernorat et comptage du Nombre_total_de_colis par gouvernorat
count_by_gouvernorat = df.groupby('Gouvernorat')['Colis'].count().reset_index()
count_by_gouvernorat = count_by_gouvernorat.rename(columns={'Colis': 'Nombre_total_de_colis'})

# Fusionner les DataFrames sum_by_gouvernorat et count_by_gouvernorat sur la colonne Gouvernorat
result = pd.merge(sum_by_gouvernorat, count_by_gouvernorat, on='Gouvernorat')

# Filtrer les lignes où le statut est "Livré" et compter le Nombre_de_Colis_Livrés par gouvernorat
colis_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_livres_par_gouvernorat = colis_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Livrés'})

# Ajouter une colonne avec le Nombre_de_Colis_Livrés par gouvernorat
result = pd.merge(result, colis_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Livré" et calculer la Somme_de_Cr_apres_remise_des_colis_livrés par gouvernorat
sum_cr_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_livres_par_gouvernorat = sum_cr_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et compter le Nombre_de_Colis_Retournés par gouvernorat
colis_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_retournes_par_gouvernorat = colis_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Retournés'})

# Ajouter une colonne avec le Nombre_de_Colis_Retournés par gouvernorat
result = pd.merge(result, colis_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et calculer la Somme_de_Cr_apres_remise_des_colis_retournés par gouvernorat
sum_cr_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_retournes_par_gouvernorat = sum_cr_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et compter le Nombre_de_Colis_Non_confirmés par gouvernorat
colis_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_non_confirmes_par_gouvernorat = colis_non_confirmes_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Non_confirmés'})

# Ajouter une colonne avec le Nombre_de_Colis_Non_confirmés par gouvernorat
result = pd.merge(result, colis_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et calculer la Somme_de_Cr_apres_remise_des_colis_non_confirmés par gouvernorat
sum_cr_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_non_confirmes_par_gouvernorat = sum_cr_non_confirmes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_non_confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Regroupement par gouvernorat et calcul de la Somme_de_Cr_apres_remise par gouvernorat
sum_by_gouvernorat = df.groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_by_gouvernorat = sum_by_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise'})

# Regroupement par gouvernorat et comptage du Nombre_total_de_colis par gouvernorat
count_by_gouvernorat = df.groupby('Gouvernorat')['Colis'].count().reset_index()
count_by_gouvernorat = count_by_gouvernorat.rename(columns={'Colis': 'Nombre_total_de_colis'})

# Fusionner les DataFrames sum_by_gouvernorat et count_by_gouvernorat sur la colonne Gouvernorat
result = pd.merge(sum_by_gouvernorat, count_by_gouvernorat, on='Gouvernorat')

# Filtrer les lignes où le statut est "Livré" et compter le Nombre_de_Colis_Livrés par gouvernorat
colis_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_livres_par_gouvernorat = colis_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Livrés'})

# Ajouter une colonne avec le Nombre_de_Colis_Livrés par gouvernorat
result = pd.merge(result, colis_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Livré" et calculer la Somme_de_Cr_apres_remise_des_colis_livrés par gouvernorat
sum_cr_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_livres_par_gouvernorat = sum_cr_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et compter le Nombre_de_Colis_Retournés par gouvernorat
colis_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_retournes_par_gouvernorat = colis_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Retournés'})

# Ajouter une colonne avec le Nombre_de_Colis_Retournés par gouvernorat
result = pd.merge(result, colis_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et calculer la Somme_de_Cr_apres_remise_des_colis_retournés par gouvernorat
sum_cr_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_retournes_par_gouvernorat = sum_cr_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et compter le Nombre_de_Colis_Non_confirmés par gouvernorat
colis_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_non_confirmes_par_gouvernorat = colis_non_confirmes_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_Colis_Non_confirmés'})

# Ajouter une colonne avec le Nombre_de_Colis_Non_confirmés par gouvernorat
result = pd.merge(result, colis_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et calculer la Somme_de_Cr_apres_remise_des_colis_non_confirmés par gouvernorat
sum_cr_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_non_confirmes_par_gouvernorat = sum_cr_non_confirmes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_des_colis_non_confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et compter le nombre d'hommes par gouvernorat
hommes_par_gouvernorat = df[df['Genre'] == 'Homme'].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_par_gouvernorat = hommes_par_gouvernorat.rename(columns={'Colis': 'Nombre_hommes'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis compter le nombre d'hommes dont les colis ont été livrés par gouvernorat
hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_livres_par_gouvernorat = hommes_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre_hommes_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Retour" puis compter le nombre d'hommes dont les colis ont été retournés par gouvernorat
hommes_retournes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_retournes_par_gouvernorat = hommes_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre_hommes_retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Non confirmé" puis compter le nombre d'hommes dont les colis sont non confirmés par gouvernorat
hommes_non_confirmes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_non_confirmes_par_gouvernorat = hommes_non_confirmes_par_gouvernorat.rename(columns={'Colis': 'Nombre_hommes_non_confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et compter le Nombre_de_femmes par gouvernorat
femmes_par_gouvernorat = df[df['Genre'] == 'Femme'].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_par_gouvernorat = femmes_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_femmes'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Livré" puis compter le Nombre_de_femmes dont les colis ont été livrés par gouvernorat
femmes_livrees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_livrees_par_gouvernorat = femmes_livrees_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_femmes_livrées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_livrees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis compter le Nombre_de_femmes dont les colis sont non confirmés par gouvernorat
femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_non_confirmees_par_gouvernorat = femmes_non_confirmees_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_femmes_retournées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis compter le nombre de femmes dont les colis sont non confirmés par gouvernorat
femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_non_confirmees_par_gouvernorat = femmes_non_confirmees_par_gouvernorat.rename(columns={'Colis': 'Nombre_de_femmes_non_confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis calculer la somme de Cr apres remise pour les hommes livrés par gouvernorat
sum_cr_hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_livres_par_gouvernorat = sum_cr_hommes_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_hommes_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Retour" puis calculer la somme de Cr apres remise pour les hommes retournés par gouvernorat
sum_cr_hommes_retournes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_retournes_par_gouvernorat = sum_cr_hommes_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour hommes retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Non confirmé" puis calculer la somme de Cr apres remise pour les hommes non confirmés par gouvernorat
sum_cr_hommes_non_confirmes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_non_confirmes_par_gouvernorat = sum_cr_hommes_non_confirmes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour hommes non confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Livré" puis calculer la somme de Cr apres remise pour les femmes livrées par gouvernorat
sum_cr_femmes_livrees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_livrees_par_gouvernorat = sum_cr_femmes_livrees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour femmes livrées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_livrees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Retour" puis calculer la somme de Cr apres remise pour les femmes retournées par gouvernorat
sum_cr_femmes_retournees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_retournees_par_gouvernorat = sum_cr_femmes_retournees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_retournées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_retournees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis calculer la somme de Cr apres remise pour les femmes non confirmées par gouvernorat
sum_cr_femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_non_confirmees_par_gouvernorat = sum_cr_femmes_non_confirmees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_non_confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis calculer la Somme_de_Cr_apres_remise pour les hommes livrés par gouvernorat
sum_cr_hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_livres_par_gouvernorat = sum_cr_hommes_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_hommes_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Retour" puis calculer la Somme_de_Cr_apres_remise pour les hommes retournés par gouvernorat
sum_cr_hommes_retournes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_retournes_par_gouvernorat = sum_cr_hommes_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_hommes_retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Non confirmé" puis calculer la Somme_de_Cr_apres_remise pour les hommes non confirmés par gouvernorat
sum_cr_hommes_non_confirmes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_non_confirmes_par_gouvernorat = sum_cr_hommes_non_confirmes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_hommes_non_confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Retour" puis calculer la Somme_de_Cr_apres_remise pour les femmes retournées par gouvernorat
sum_cr_femmes_retournees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_retournees_par_gouvernorat = sum_cr_femmes_retournees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_livrées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_retournees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis calculer la Somme_de_Cr_apres_remise pour les femmes non confirmées par gouvernorat
sum_cr_femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_non_confirmees_par_gouvernorat = sum_cr_femmes_non_confirmees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_non_confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis calculer la Somme_de_Cr_apres_remise pour les hommes livrés par gouvernorat
sum_cr_hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_livres_par_gouvernorat = sum_cr_hommes_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_hommes_livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_hommes_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)
# Filtrer les lignes où le genre est "Femme" et le statut est "Livré" puis calculer la Somme_de_Cr_apres_remise pour les femmes livrées par gouvernorat
sum_cr_femmes_livrees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_livrees_par_gouvernorat = sum_cr_femmes_livrees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_livrées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_livrees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Retour" puis calculer la Somme_de_Cr_apres_remise pour les femmes retournées par gouvernorat
sum_cr_femmes_retournees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_retournees_par_gouvernorat = sum_cr_femmes_retournees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_livrées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_retournees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis calculer la Somme_de_Cr_apres_remise pour les femmes non confirmées par gouvernorat
sum_cr_femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_non_confirmees_par_gouvernorat = sum_cr_femmes_non_confirmees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme_de_Cr_apres_remise_pour_femmes_non_confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Define the desired columns for printing and saving
desired_columns = [
    'Gouvernorat',
    'Nombre_total_de_colis',
    'Somme_de_Cr_apres_remise',
    'Nombre_de_Colis_Livrés',
    'Somme_de_Cr_apres_remise_des_colis_livrés',
    'Nombre_de_Colis_Retournés',
    'Somme_de_Cr_apres_remise_des_colis_retournés',
    'Nombre_de_Colis_Non_confirmés',
    'Somme_de_Cr_apres_remise_des_colis_non_confirmés',
    'Nombre_hommes',
    'Nombre_de_femmes',
    'Nombre_hommes_livrés',
    'Somme_de_Cr_apres_remise_pour_hommes_livrés',
    'Nombre_hommes_retournés',
    'Somme_de_Cr_apres_remise_pour_hommes_retournés',
    'Nombre_hommes_non_confirmés',
    'Somme_de_Cr_apres_remise_pour_hommes_non_confirmés',
    'Nombre_de_femmes_livrées',
    'Somme_de_Cr_apres_remise_pour_femmes_livrées',
    'Nombre_de_femmes_retournées',
    'Somme_de_Cr_apres_remise_pour_femmes_retournées',
    'Nombre_de_femmes_non_confirmées',
    'Somme_de_Cr_apres_remise_pour_femmes_non_confirmées'
]

# Check which columns are actually in the result DataFrame
existing_columns = [col for col in desired_columns if col in result.columns]

# Print the DataFrame with existing columns
print(tabulate(result[existing_columns], headers='keys', tablefmt='pretty'))

# Save the result to a CSV file
result[existing_columns].to_csv('stats.csv', index=False)

print("Data saved to 'stats.csv'")

# Données sur les gouvernorats
gouvernorats = ['Tunis', 'Ariana', 'Ben Arous', 'Manouba', 'Nabeul', 'Zaghouan', 'Bizerte', 'Béja', 'Jendouba', 'Le Kef', 'Siliana', 'Kairouan', 'Kasserine', 'Sidi Bouzid', 'Sousse', 'Mahdia', 'Monastir', 'Gabès', 'Médenine', 'Gafsa', 'Tozeur', 'Kébili', 'Tataouine', 'Seliana']

# Convertir la colonne 'Date' en type datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extraire le jour et le mois dans de nouvelles colonnes
df['Jour'] = df['Date'].dt.day
df['Mois'] = df['Date'].dt.month

# Filtrer les données pour le 29 novembre
df_nov29 = df[(df['Jour'] == 29) & (df['Mois'] == 11)]

# Compter le nombre de colis pour chaque gouvernorat le 29 novembre
count_by_governorate_nov29 = df_nov29.groupby('Gouvernorat').size().reset_index(name='Black_Friday')

# Filtrer les données pour la période de la Saint_Valentin (30 janvier - 14 février)
df_valentine = df[((df['Jour'] >= 30) & (df['Mois'] == 1)) | ((df['Jour'] <= 14) & (df['Mois'] == 2))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la Saint_Valentin
count_by_governorate_valentine = df_valentine.groupby('Gouvernorat').size().reset_index(name='Saint_Valentin')

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.DataFrame({'Gouvernorat': gouvernorats})

# Fusionner avec le DataFrame des comptages du Black_Friday pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_nov29, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis le 29 novembre) par 0
merged_df['Black_Friday'].fillna(0, inplace=True)

# Fusionner avec le DataFrame des comptages de la Saint_Valentin pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_valentine, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la Saint_Valentin) par 0
merged_df['Saint_Valentin'].fillna(0, inplace=True)

# Filtrer les données pour la période des Soldes d'hiver (1 février - 13 mars)
df_soldes_hiver = df[((df['Jour'] >= 1) & (df['Mois'] == 2)) | ((df['Jour'] <= 13) & (df['Mois'] == 3))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période des Soldes d'hiver
count_by_governorate_soldes_hiver = df_soldes_hiver.groupby('Gouvernorat').size().reset_index(name='Soldes_Hiver')

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_soldes_hiver, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période des Soldes d'hiver) par 0
merged_df['Soldes_Hiver'].fillna(0, inplace=True)

# Filtrer les données pour la période des Soldes d'été (7 août - 17 septembre)
df_soldes_ete = df[((df['Jour'] >= 7) & (df['Mois'] == 8)) | ((df['Jour'] <= 17) & (df['Mois'] == 9))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période des Soldes d'été
count_by_governorate_soldes_ete = df_soldes_ete.groupby('Gouvernorat').size().reset_index(name='Soldes_Été')

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_soldes_ete, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période des Soldes d'été) par 0
merged_df['Soldes_Été'].fillna(0, inplace=True)

# Filtrer les données pour la période de la fête des mères (12 mai - 26 mai)
df_mothers_day = df[((df['Jour'] >= 12) & (df['Mois'] == 5)) | ((df['Jour'] <= 26) & (df['Mois'] == 5))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la fête des mères
count_by_governorate_mothers_day = df_mothers_day.groupby('Gouvernorat').size().reset_index(name="Mother_Day")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_mothers_day, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la fête des mères) par 0
merged_df["Mother_Day"].fillna(0, inplace=True)

# Filtrer les données pour la période de la Journée de la Femme (22 février - 8 mars)
df_womens_day = df[((df['Jour'] >= 22) & (df['Mois'] == 2)) | ((df['Jour'] <= 8) & (df['Mois'] == 3))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la Journée de la Femme
count_by_governorate_womens_day = df_womens_day.groupby('Gouvernorat').size().reset_index(name="Woman_Day")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_womens_day, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la Journée de la Femme) par 0
merged_df["Woman_Day"].fillna(0, inplace=True)

# Filtrer les données pour la période de la fête des Pères (1er juin - 16 juin)
df_fathers_day = df[((df['Jour'] >= 1) & (df['Mois'] == 6)) | ((df['Jour'] <= 16) & (df['Mois'] == 6))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la fête des Pères
count_by_governorate_fathers_day = df_fathers_day.groupby('Gouvernorat').size().reset_index(name="Father_Day")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_fathers_day, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la fête des Pères) par 0
merged_df["Father_Day"].fillna(0, inplace=True)

# Filtrer les données pour la période de Noël (10 décembre - 25 décembre)
df_noel = df[((df['Jour'] >= 10) & (df['Mois'] == 12)) | ((df['Jour'] <= 25) & (df['Mois'] == 12))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de Noël
count_by_governorate_noel = df_noel.groupby('Gouvernorat').size().reset_index(name="Noël")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_noel, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de Noël) par 0
merged_df['Noël'].fillna(0, inplace=True)

# Afficher le résultat
print(tabulate(merged_df[['Gouvernorat', 'Black_Friday', 'Saint_Valentin', 'Soldes_Hiver', 'Soldes_Été', "Mother_Day", "Woman_Day", "Father_Day", 'Noël']], headers='keys', tablefmt='pretty'))

# Save the merged DataFrame to a CSV file
merged_df.to_csv('Hollydays.csv', index=False)

# Print a message indicating that the file has been saved
print("Merged data saved to 'Hollyda.csv'")