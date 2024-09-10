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
# Regroupement par gouvernorat et calcul de la somme de Cr apres remise par gouvernorat
sum_by_gouvernorat = df.groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_by_gouvernorat = sum_by_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise'})

# Regroupement par gouvernorat et comptage du nombre total de colis par gouvernorat
count_by_gouvernorat = df.groupby('Gouvernorat')['Colis'].count().reset_index()
count_by_gouvernorat = count_by_gouvernorat.rename(columns={'Colis': 'Nombre total de colis'})

# Fusionner les DataFrames sum_by_gouvernorat et count_by_gouvernorat sur la colonne Gouvernorat
result = pd.merge(sum_by_gouvernorat, count_by_gouvernorat, on='Gouvernorat')

# Filtrer les lignes où le statut est "Livré" et compter le nombre de colis livrés par gouvernorat
colis_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_livres_par_gouvernorat = colis_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Livrés'})

# Ajouter une colonne avec le nombre de colis livrés par gouvernorat
result = pd.merge(result, colis_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Livré" et calculer la somme de Cr apres remise des colis livrés par gouvernorat
sum_cr_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_livres_par_gouvernorat = sum_cr_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et compter le nombre de colis retournés par gouvernorat
colis_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_retournes_par_gouvernorat = colis_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Retournés'})

# Ajouter une colonne avec le nombre de colis retournés par gouvernorat
result = pd.merge(result, colis_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et calculer la somme de Cr apres remise des colis retournés par gouvernorat
sum_cr_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_retournes_par_gouvernorat = sum_cr_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Regroupement par gouvernorat et calcul de la somme de Cr apres remise par gouvernorat
sum_by_gouvernorat = df.groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_by_gouvernorat = sum_by_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise'})

# Regroupement par gouvernorat et comptage du nombre total de colis par gouvernorat
count_by_gouvernorat = df.groupby('Gouvernorat')['Colis'].count().reset_index()
count_by_gouvernorat = count_by_gouvernorat.rename(columns={'Colis': 'Nombre total de colis'})

# Fusionner les DataFrames sum_by_gouvernorat et count_by_gouvernorat sur la colonne Gouvernorat
result = pd.merge(sum_by_gouvernorat, count_by_gouvernorat, on='Gouvernorat')

# Filtrer les lignes où le statut est "Livré" et compter le nombre de colis livrés par gouvernorat
colis_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_livres_par_gouvernorat = colis_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Livrés'})

# Ajouter une colonne avec le nombre de colis livrés par gouvernorat
result = pd.merge(result, colis_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Livré" et calculer la somme de Cr apres remise des colis livrés par gouvernorat
sum_cr_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_livres_par_gouvernorat = sum_cr_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et compter le nombre de colis retournés par gouvernorat
colis_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_retournes_par_gouvernorat = colis_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Retournés'})

# Ajouter une colonne avec le nombre de colis retournés par gouvernorat
result = pd.merge(result, colis_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et calculer la somme de Cr apres remise des colis retournés par gouvernorat
sum_cr_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_retournes_par_gouvernorat = sum_cr_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et compter le nombre de colis non confirmés par gouvernorat
colis_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_non_confirmes_par_gouvernorat = colis_non_confirmes_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Non confirmés'})

# Ajouter une colonne avec le nombre de colis non confirmés par gouvernorat
result = pd.merge(result, colis_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et calculer la somme de Cr apres remise des colis non confirmés par gouvernorat
sum_cr_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_non_confirmes_par_gouvernorat = sum_cr_non_confirmes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis non confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Regroupement par gouvernorat et calcul de la somme de Cr apres remise par gouvernorat
sum_by_gouvernorat = df.groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_by_gouvernorat = sum_by_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise'})

# Regroupement par gouvernorat et comptage du nombre total de colis par gouvernorat
count_by_gouvernorat = df.groupby('Gouvernorat')['Colis'].count().reset_index()
count_by_gouvernorat = count_by_gouvernorat.rename(columns={'Colis': 'Nombre total de colis'})

# Fusionner les DataFrames sum_by_gouvernorat et count_by_gouvernorat sur la colonne Gouvernorat
result = pd.merge(sum_by_gouvernorat, count_by_gouvernorat, on='Gouvernorat')

# Filtrer les lignes où le statut est "Livré" et compter le nombre de colis livrés par gouvernorat
colis_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_livres_par_gouvernorat = colis_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Livrés'})

# Ajouter une colonne avec le nombre de colis livrés par gouvernorat
result = pd.merge(result, colis_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Livré" et calculer la somme de Cr apres remise des colis livrés par gouvernorat
sum_cr_livres_par_gouvernorat = df[df['Statut'] == 'Livré'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_livres_par_gouvernorat = sum_cr_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et compter le nombre de colis retournés par gouvernorat
colis_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_retournes_par_gouvernorat = colis_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Retournés'})

# Ajouter une colonne avec le nombre de colis retournés par gouvernorat
result = pd.merge(result, colis_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Retour" et calculer la somme de Cr apres remise des colis retournés par gouvernorat
sum_cr_retournes_par_gouvernorat = df[df['Statut'] == 'Retour'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_retournes_par_gouvernorat = sum_cr_retournes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et compter le nombre de colis non confirmés par gouvernorat
colis_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Colis'].count().reset_index()
colis_non_confirmes_par_gouvernorat = colis_non_confirmes_par_gouvernorat.rename(columns={'Colis': 'Nombre de Colis Non confirmés'})

# Ajouter une colonne avec le nombre de colis non confirmés par gouvernorat
result = pd.merge(result, colis_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le statut est "Non confirmé" et calculer la somme de Cr apres remise des colis non confirmés par gouvernorat
sum_cr_non_confirmes_par_gouvernorat = df[df['Statut'] == 'Non confirmé'].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_non_confirmes_par_gouvernorat = sum_cr_non_confirmes_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise des colis non confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et compter le nombre d'hommes par gouvernorat
hommes_par_gouvernorat = df[df['Genre'] == 'Homme'].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_par_gouvernorat = hommes_par_gouvernorat.rename(columns={'Colis': 'Nombre d\'hommes'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis compter le nombre d'hommes dont les colis ont été livrés par gouvernorat
hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_livres_par_gouvernorat = hommes_livres_par_gouvernorat.rename(columns={'Colis': 'Nombre d\'hommes livrés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_livres_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Retour" puis compter le nombre d'hommes dont les colis ont été retournés par gouvernorat
hommes_retournes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_retournes_par_gouvernorat = hommes_retournes_par_gouvernorat.rename(columns={'Colis': 'Nombre d\'hommes retournés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_retournes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Non confirmé" puis compter le nombre d'hommes dont les colis sont non confirmés par gouvernorat
hommes_non_confirmes_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Colis'].count().reset_index()
hommes_non_confirmes_par_gouvernorat = hommes_non_confirmes_par_gouvernorat.rename(columns={'Colis': 'Nombre d\'hommes non confirmés'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, hommes_non_confirmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et compter le nombre de femmes par gouvernorat
femmes_par_gouvernorat = df[df['Genre'] == 'Femme'].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_par_gouvernorat = femmes_par_gouvernorat.rename(columns={'Colis': 'Nombre de femmes'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Livré" puis compter le nombre de femmes dont les colis ont été livrés par gouvernorat
femmes_livrees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_livrees_par_gouvernorat = femmes_livrees_par_gouvernorat.rename(columns={'Colis': 'Nombre de femmes livrées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_livrees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Retour" puis compter le nombre de femmes dont les colis ont été retournés par gouvernorat
femmes_retournees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Retour')].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_retournees_par_gouvernorat = femmes_retournees_par_gouvernorat.rename(columns={'Colis': 'Nombre de femmes retournées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_retournees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis compter le nombre de femmes dont les colis sont non confirmés par gouvernorat
femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Colis'].count().reset_index()
femmes_non_confirmees_par_gouvernorat = femmes_non_confirmees_par_gouvernorat.rename(columns={'Colis': 'Nombre de femmes non confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis calculer la somme de Cr apres remise pour les hommes livrés par gouvernorat
sum_cr_hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_livres_par_gouvernorat = sum_cr_hommes_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour hommes livrés'})

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
sum_cr_femmes_retournees_par_gouvernorat = sum_cr_femmes_retournees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour femmes retournées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_retournees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis calculer la somme de Cr apres remise pour les femmes non confirmées par gouvernorat
sum_cr_femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_non_confirmees_par_gouvernorat = sum_cr_femmes_non_confirmees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour femmes non confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Homme" et le statut est "Livré" puis calculer la somme de Cr apres remise pour les hommes livrés par gouvernorat
sum_cr_hommes_livres_par_gouvernorat = df[(df['Genre'] == 'Homme') & (df['Statut'] == 'Livré')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_hommes_livres_par_gouvernorat = sum_cr_hommes_livres_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour hommes livrés'})

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
sum_cr_femmes_retournees_par_gouvernorat = sum_cr_femmes_retournees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour femmes retournées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_retournees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Filtrer les lignes où le genre est "Femme" et le statut est "Non confirmé" puis calculer la somme de Cr apres remise pour les femmes non confirmées par gouvernorat
sum_cr_femmes_non_confirmees_par_gouvernorat = df[(df['Genre'] == 'Femme') & (df['Statut'] == 'Non confirmé')].groupby('Gouvernorat')['Cr apres remise'].sum().reset_index()
sum_cr_femmes_non_confirmees_par_gouvernorat = sum_cr_femmes_non_confirmees_par_gouvernorat.rename(columns={'Cr apres remise': 'Somme de Cr apres remise pour femmes non confirmées'})

# Fusionner le résultat avec le DataFrame principal sur la colonne Gouvernorat
result = pd.merge(result, sum_cr_femmes_non_confirmees_par_gouvernorat, on='Gouvernorat', how='left').fillna(0)

# Define the desired columns for printing and saving
desired_columns = [
    'Gouvernorat',
    'Nombre total de colis',
    'Somme de Cr apres remise',
    'Nombre de Colis Livrés',
    'Somme de Cr apres remise des colis livrés',
    'Nombre de Colis Retournés',
    'Somme de Cr apres remise des colis retournés',
    'Nombre de Colis Non confirmés',
    'Somme de Cr apres remise des colis non confirmés',
    'Nombre d\'hommes',
    'Nombre de femmes',
    'Nombre d\'hommes livrés',
    'Somme de Cr apres remise pour hommes livrés',
    'Nombre d\'hommes retournés',
    'Somme de Cr apres remise pour hommes retournés',
    'Nombre d\'hommes non confirmés',
    'Somme de Cr apres remise pour hommes non confirmés',
    'Nombre de femmes livrées',
    'Somme de Cr apres remise pour femmes livrées',
    'Nombre de femmes retournées',
    'Somme de Cr apres remise pour femmes retournées',
    'Nombre de femmes non confirmées',
    'Somme de Cr apres remise pour femmes non confirmées'
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
count_by_governorate_nov29 = df_nov29.groupby('Gouvernorat').size().reset_index(name='Black-Friday')

# Filtrer les données pour la période de la Saint-Valentin (30 janvier - 14 février)
df_valentine = df[((df['Jour'] >= 30) & (df['Mois'] == 1)) | ((df['Jour'] <= 14) & (df['Mois'] == 2))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la Saint-Valentin
count_by_governorate_valentine = df_valentine.groupby('Gouvernorat').size().reset_index(name='Saint-Valentin')

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.DataFrame({'Gouvernorat': gouvernorats})

# Fusionner avec le DataFrame des comptages du Black Friday pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_nov29, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis le 29 novembre) par 0
merged_df['Black-Friday'].fillna(0, inplace=True)

# Fusionner avec le DataFrame des comptages de la Saint-Valentin pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_valentine, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la Saint-Valentin) par 0
merged_df['Saint-Valentin'].fillna(0, inplace=True)

# Filtrer les données pour la période des Soldes d'hiver (1 février - 13 mars)
df_soldes_hiver = df[((df['Jour'] >= 1) & (df['Mois'] == 2)) | ((df['Jour'] <= 13) & (df['Mois'] == 3))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période des Soldes d'hiver
count_by_governorate_soldes_hiver = df_soldes_hiver.groupby('Gouvernorat').size().reset_index(name='Soldes-Hiver')

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_soldes_hiver, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période des Soldes d'hiver) par 0
merged_df['Soldes-Hiver'].fillna(0, inplace=True)

# Filtrer les données pour la période des Soldes d'été (7 août - 17 septembre)
df_soldes_ete = df[((df['Jour'] >= 7) & (df['Mois'] == 8)) | ((df['Jour'] <= 17) & (df['Mois'] == 9))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période des Soldes d'été
count_by_governorate_soldes_ete = df_soldes_ete.groupby('Gouvernorat').size().reset_index(name='Soldes-Été')

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_soldes_ete, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période des Soldes d'été) par 0
merged_df['Soldes-Été'].fillna(0, inplace=True)

# Filtrer les données pour la période de la fête des mères (12 mai - 26 mai)
df_mothers_day = df[((df['Jour'] >= 12) & (df['Mois'] == 5)) | ((df['Jour'] <= 26) & (df['Mois'] == 5))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la fête des mères
count_by_governorate_mothers_day = df_mothers_day.groupby('Gouvernorat').size().reset_index(name="Mother's-Day")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_mothers_day, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la fête des mères) par 0
merged_df["Mother's-Day"].fillna(0, inplace=True)

# Filtrer les données pour la période de la Journée de la Femme (22 février - 8 mars)
df_womens_day = df[((df['Jour'] >= 22) & (df['Mois'] == 2)) | ((df['Jour'] <= 8) & (df['Mois'] == 3))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la Journée de la Femme
count_by_governorate_womens_day = df_womens_day.groupby('Gouvernorat').size().reset_index(name="Woman's-Day")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_womens_day, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la Journée de la Femme) par 0
merged_df["Woman's-Day"].fillna(0, inplace=True)

# Filtrer les données pour la période de la fête des Pères (1er juin - 16 juin)
df_fathers_day = df[((df['Jour'] >= 1) & (df['Mois'] == 6)) | ((df['Jour'] <= 16) & (df['Mois'] == 6))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de la fête des Pères
count_by_governorate_fathers_day = df_fathers_day.groupby('Gouvernorat').size().reset_index(name="Father's-Day")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_fathers_day, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de la fête des Pères) par 0
merged_df["Father's-Day"].fillna(0, inplace=True)

# Filtrer les données pour la période de Noël (10 décembre - 25 décembre)
df_noel = df[((df['Jour'] >= 10) & (df['Mois'] == 12)) | ((df['Jour'] <= 25) & (df['Mois'] == 12))]

# Compter le nombre de colis pour chaque gouvernorat pendant la période de Noël
count_by_governorate_noel = df_noel.groupby('Gouvernorat').size().reset_index(name="Noël")

# Fusionner avec le DataFrame d'origine pour inclure tous les gouvernorats
merged_df = pd.merge(merged_df, count_by_governorate_noel, on='Gouvernorat', how='left')

# Remplacer les valeurs manquantes (gouvernorats sans colis pendant la période de Noël) par 0
merged_df['Noël'].fillna(0, inplace=True)

# Afficher le résultat
print(tabulate(merged_df[['Gouvernorat', 'Black-Friday', 'Saint-Valentin', 'Soldes-Hiver', 'Soldes-Été', "Mother's-Day", "Woman's-Day", "Father's-Day", 'Noël']], headers='keys', tablefmt='pretty'))

# Save the merged DataFrame to a CSV file
merged_df.to_csv('Hollydays.csv', index=False)

# Print a message indicating that the file has been saved
print("Merged data saved to 'Hollyda.csv'")