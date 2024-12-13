import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize DataFrame for patient data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'Nom', 'Prenom', 'Date_naissance', 'Indication', 'Debut_traitement', 'Fin_traitement', 'Actif'
    ])

data = st.session_state.data

# Page title
st.set_page_config(page_title="Application Patient", layout="wide")
st.title("Application Patient")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["Ajouter un Patient", "Tableau de Bord"])

if menu == "Ajouter un Patient":
    st.header("Ajouter un Patient")
    with st.form("add_patient"):
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        date_naissance = st.date_input("Date de naissance (facultatif)")
        indications = [
            'ALR Post Opératoire', 'Antibio intraveineuse', 'Hydratation Diffuseur',
            'Hydratation Pompe', 'Perfusion Diffuseur', 'Perfusion Gravité',
            'Perfusion Pompe', 'Post op/RAAC', 'Solumédrol',
            "Entretien gastrostomie en vu d'une NED", 'Entretien PICC LINE/VVC',
            'Immuno IV', 'Immuno SC', 'Ned Pompe', 'NPAD', 'PCA',
            'Chimiothérapie', 'Radiothérapie', 'Suivi post-opératoire', 'Traitement palliatif'
        ]
        indication = st.selectbox("Indication", indications)
        debut_traitement = st.date_input("Début du traitement")
        fin_traitement = st.date_input("Fin du traitement", datetime.today())
        actif = st.radio("Actif/Inactif", ["Actif", "Inactif"])

        submitted = st.form_submit_button("Ajouter")
        if submitted:
            new_data = {
                'Nom': nom,
                'Prenom': prenom,
                'Date_naissance': date_naissance.strftime('%Y-%m-%d'),
                'Indication': indication,
                'Debut_traitement': debut_traitement.strftime('%Y-%m-%d'),
                'Fin_traitement': fin_traitement.strftime('%Y-%m-%d'),
                'Actif': actif
            }
            data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
            st.session_state.data = data
            st.success("Patient ajouté avec succès!")

elif menu == "Tableau de Bord":
    st.header("Tableau de Bord")
    if data.empty:
        st.warning("Aucun patient enregistré.")
    else:
        # Display statistics
        active_count = len(data[data['Actif'] == 'Actif'])
        inactive_count = len(data[data['Actif'] == 'Inactif'])
        st.subheader("Statistiques générales")
        st.write(f"Nombre total de patients actifs : {active_count}")
        st.write(f"Nombre total de patients inactifs : {inactive_count}")

        # Patients per indication
        st.subheader("Répartition des indications")
        indication_counts = data['Indication'].value_counts()
        st.write(indication_counts)

        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(indication_counts, labels=indication_counts.index, autopct='%1.1f%%')
        ax.set_title("Répartition des indications")
        st.pyplot(fig)

        # Display full data
        st.subheader("Données complètes des patients")
        st.dataframe(data)

