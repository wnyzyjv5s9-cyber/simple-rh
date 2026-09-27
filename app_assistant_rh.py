import streamlit as st

# ==============================================================================
# CONFIGURATION COMMERCIALE - PILOTE RH
# ==============================================================================
NOM_APPLICATION = "Pilote RH"
LIEN_PAIEMENT_STRIPE = "https://buy.stripe.com/fZu5kE8ZWfYw1ll1FFe7m00"

# Base de données des abonnés officiels (Identifiant: {Nom, Mot de passe, Statut})
BASE_DONNEES_CLIENTS = {
    "dirigeant1": {"nom": "Société Alpha", "pass": "alpha2026", "statut": "Actif"},
    "patron2": {"nom": "Boulangerie Louise", "pass": "louise2026", "statut": "Actif"},
    "test_pme": {"nom": "Entreprise Demo", "pass": "demo123", "statut": "Suspendu"},
}

st.set_page_config(page_title=NOM_APPLICATION, page_icon="💼", layout="wide")

# Gestion de l'état de la page (Connexion, Inscription ou Application)
if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False
    st.session_state["client_id"] = None
if "page_inscription" not in st.session_state:
    st.session_state["page_inscription"] = False

# ==============================================================================
# ÉCRAN 1 : FORMULAIRE D'INSCRIPTION AUTOMATIQUE
# ==============================================================================
if st.session_state["page_inscription"]:
    st.title(f"🚀 Rejoindre {NOM_APPLICATION}")
    st.subheader("Activez votre outil RH en moins de 2 minutes")
    
    with st.form("form_inscription"):
        nom_complet = st.text_input("Votre Prénom et Nom *")
        nom_pme = st.text_input("Nom de votre Entreprise *")
        email_pro = st.text_input("Adresse Email professionnelle *")
        tel_pro = st.text_input("Numéro de Téléphone *")
        
        formule = st.radio(
            "Choisissez votre formule d'abonnement :",
            ["Abonnement Mensuel - 49 € HT / mois (Sans engagement)", "Abonnement Annuel - 390 € HT / an (2 mois GRATUITS)"]
        )
        
        bouton_valider = st.form_submit_button("Valider ma demande d'accès", use_container_width=True)
        
        if bouton_valider:
            if nom_complet and nom_pme and email_pro and tel_pro:
                st.success(f"🎉 Merci {nom_complet} ! Votre demande d'inscription pour {nom_pme} a bien été enregistrée.")
                st.info("💳 ÉTAPE FINALE : Pour activer immédiatement vos accès, veuillez procéder au règlement sécurisé.")
                st.markdown(f"[➡️ CLIQUEZ ICI POUR PAYER VOTRE ABONNEMENT SUR STRIPE]({LIEN_PAIEMENT_STRIPE})")
                st.caption("Une fois le paiement validé, notre équipe vous enverra vos codes d'accès par SMS et Email sous 10 minutes.")
            else:
                st.error("❌ Veuillez remplir tous les champs obligatoires (marqués d'une *).")
                
    if st.button("⬅️ Retour à l'écran de connexion"):
        st.session_state["page_inscription"] = False
        st.rerun()
    st.stop()

# ==============================================================================
# ÉCRAN 2 : INTERFACE DE CONNEXION SÉCURISÉE
# ==============================================================================
if not st.session_state["authentifie"]:
    st.title(f"🔑 Connexion - {NOM_APPLICATION}")
    st.subheader("Espace Client Entreprise")
    
    identifiant = st.text_input("Identifiant Client", key="user_id")
    mot_de_passe = st.text_input("Mot de passe", type="password", key="user_pass")
    
    if st.button("Se connecter", use_container_width=True):
        if identifiant in BASE_DONNEES_CLIENTS and BASE_DONNEES_CLIENTS[identifiant]["pass"] == mot_de_passe:
            client_infos = BASE_DONNEES_CLIENTS[identifiant]
            if client_infos["statut"] == "Actif":
                st.session_state["authentifie"] = True
                st.session_state["client_id"] = identifiant
                st.success(f"Bienvenue, {client_infos['nom']} !")
                st.rerun()
            else:
                st.error("❌ Votre abonnement est suspendu. Veuillez régulariser votre situation.")
                st.markdown(f"[🔗 Débloquer mon compte et régulariser sur Stripe]({LIEN_PAIEMENT_STRIPE})")
        else:
            st.error("Identifiant ou mot de passe incorrect.")
            
    st.markdown("---")
    st.write(" Vous êtes un nouveau client ?")
    if st.button("Créer un compte et s'abonner à Pilote RH", type="primary"):
        st.session_state["page_inscription"] = True
        st.rerun()
    st.stop()

# ==============================================================================
# ÉCRAN 3 : INTERFACE CONSEIL RH (CONNEXION RÉUSSIE)
# ==============================================================================
client_id = st.session_state["client_id"]
nom_entreprise = BASE_DONNEES_CLIENTS[client_id]["nom"]

st.sidebar.title(f"💼 {NOM_APPLICATION}")
st.sidebar.write(f"🏢 Client : **{nom_entreprise}**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Menu Principal",
    [
        "Tableau de bord & Seuils",
        "Simulateur de Coût d'Embauche",
        "Suivi des Congés & Absences",
        "Trame d'Entretien Annuel",
        "Entretien Professionnel (2 ans)"
    ]
)

if st.sidebar.button("Se déconnecter"):
    st.session_state["authentifie"] = False
    st.session_state["client_id"] = None
    st.rerun()

# --- MODULE 1 : TABLEAU DE BORD ---
if menu == "Tableau de bord & Seuils":
    st.header("📊 Tableau de Bord & Obligations Légales")
    effectif = st.number_input("Indiquez l'effectif actuel de votre entreprise (ETP) :", min_value=1, value=5)
    st.subheader("📋 Vos obligations majeures")
    st.markdown("✅ **Document Unique (DUERP) :** Obligatoire dès le 1er salarié.")
    st.markdown("✅ **Médecine du travail :** Suivi individuel obligatoire.")
    st.markdown("✅ **Registre Unique du Personnel :** Obligatoire dès le 1er salarié.")
    
    if effectif >= 11:
        st.error("⚠️ **Alerte Seuil 11 salariés franchi :** Élections du CSE obligatoires.")
    else:
        st.info("💡 **Seuil 11 salariés :** Prochaine étape critique pour la mise en place du CSE.")

# --- MODULE 2 : COÛT D'EMBAUCHE ---
elif menu == "Simulateur de Coût d'Embauche":
    st.header("🧮 Simulateur de Coût d'Embauche Simplifié")
    salaire_brut = st.number_input("Salaire mensuel Brut proposé (€) :", min_value=0, value=2200)
    charges_patronales_brutes = salaire_brut * 0.42
    reduction_fillon = salaire_brut * 0.18 if salaire_brut < 2800 else 0.0
    salaire_net_estime = salaire_brut * 0.78
    cout_total_mensuel = salaire_brut + charges_patronales_brutes - reduction_fillon
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Salaire NET Estimé", f"{salaire_net_estime:,.2f} €")
    with col2:
        st.metric("COÛT TOTAL MENSUEL ESTIME", f"{cout_total_mensuel:,.2f} €")

# --- MODULE 3 : CONGÉS ---
elif menu == "Suivi des Congés & Absences":
    st.header("📅 Simulateur de Solde de Congés Payés")
    acquis = st.number_input("Jours acquis :", min_value=0.0, value=25.0, step=0.5)
    pris = st.number_input("Jours demandés :", min_value=0.0, value=5.0, step=0.5)
    solde = acquis - pris
    if solde < 0:
        st.error(f"🚨 Solde insuffisant ! Manque {abs(solde)} jours.")
    else:
        st.success(f"✅ Demande validable. Solde restant : {solde} jours.")

# --- MODULE 4 : ENTRETIEN ANNUEL ---
elif menu == "Trame d'Entretien Annuel":
    st.header("📝 Générateur de Trame d'Entretien Annuel d'Évaluation")
    nom_salarie = st.text_input("Nom & Prénom du Salarié :", "Jean Dupont")
    poste = st.text_input("Poste occupé :", "Conseiller Clientèle")
    reussites = st.text_area("Principales réussites :")
    objectifs = st.text_area("Objectifs professionnels :")
    
    texte_entretien = f"ENTRETIEN ANNUEL\nEntreprise: {nom_entreprise}\nSalarie: {nom_salarie}\nPoste: {poste}\nReussites: {reussites}\nObjectifs: {objectifs}"
    st.download_button(label="📥 Télécharger (.txt)", data=texte_entretien, file_name=f"Entretien_{nom_salarie}.txt")

# --- MODULE 5 : ENTRETIEN PRO ---
elif menu == "Entretien Professionnel (2 ans)":
    st.header("📋 Générateur d'Entretien Professionnel Obligatoire")
    nom_salarie_pro = st.text_input("Nom & Prénom du Salarié :", "Marie Martin")
    souhaits = st.text_area("Souhaits d'évolution :")
    
    texte_pro = f"ENTRETIEN PROFESSIONNEL\nEntreprise: {nom_entreprise}\nSalarie: {nom_salarie_pro}\nSouhaits: {souhaits}"
    st.download_button(label="📥 Télécharger (.txt)", data=texte_pro, file_name=f"Entretien_Pro_{nom_salarie_pro}.txt")
