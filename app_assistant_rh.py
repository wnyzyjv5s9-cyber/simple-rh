import streamlit as st

# ==============================================================================
# CONFIGURATION ET BASE DE DONNÉES CLIENTS (À PERSONNALISER)
# ==============================================================================
# Nom de votre application commerciale
NOM_APPLICATION = "Assistant RH PME"

# Lien de paiement Stripe (Remplacez par votre vrai lien Stripe créé sur stripe.com)
LIEN_PAIEMENT_STRIPE = "https://stripe.com"

# Base de données simulée des abonnés (Identifiant: {Nom, Mot de passe, Statut})
BASE_DONNEES_CLIENTS = {
    "dirigeant1": {"nom": "Société Alpha", "pass": "alpha2026", "statut": "Actif"},
    "patron2": {"nom": "Boulangerie Louise", "pass": "louise2026", "statut": "Actif"},
    "test_pme": {"nom": "Entreprise Demo", "pass": "demo123", "statut": "Suspendu"},
}

# ==============================================================================
# INTERFACE DE CONNEXION / SÉCURITÉ SAAS
# ==============================================================================
st.set_page_config(page_title=NOM_APPLICATION, page_icon="💼", layout="wide")

if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False
    st.session_state["client_id"] = None

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
                st.error("❌ Votre abonnement est actuellement suspendu. Veuillez régulariser votre situation.")
                st.markdown(f"[🔗 Débloquer mon compte et régulariser sur Stripe]({LIEN_PAIEMENT_STRIPE})")
        else:
            st.error("Identifiant ou mot de passe incorrect.")
            
    st.markdown("---")
    st.caption("Vous n'avez pas encore de compte ? Contactez notre service commercial pour activer votre accès.")
    st.stop()

# ==============================================================================
# INTERFACE PRINCIPALE DE L'APPLICATION (ACCÈS AUTORISÉ)
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

# ------------------------------------------------------------------------------
# ONGLET 1 : TABLEAU DE BORD & SEUILS
# ------------------------------------------------------------------------------
if menu == "Tableau de bord & Seuils":
    st.header("📊 Tableau de Bord & Obligations Légales")
    
    effectif = st.number_input("Indiquez l'effectif actuel de votre entreprise (ETP) :", min_value=1, value=5)
    
    st.subheader("📋 Vos obligations majeures")
    
    # Obligations de base pour toutes les entreprises
    st.markdown("✅ **Document Unique (DUERP) :** Obligatoire dès le 1er salarié. Doit être mis à jour régulièrement.")
    st.markdown("✅ **Médecine du travail :** Suivi individuel obligatoire de l'état de santé de chaque travailleur.")
    st.markdown("✅ **Registre Unique du Personnel :** Obligatoire. Doit lister les salariés par ordre d'embauche.")
    
    # Alertes de seuils dynamiques
    if effectif >= 11:
        st.error("⚠️ **Alerte Seuil 11 salariés franchi :** Vous devez obligatoirement mettre en place le Comité Économique et Social (CSE) si ce seuil est atteint pendant 12 mois consécutifs.")
    else:
        st.info("💡 **Seuil 11 salariés :** Prochaine étape critique. Dès 11 salariés, l'organisation des élections du CSE devient obligatoire.")
        
    if effectif >= 50:
        st.error("⚠️ **Alerte Seuil 50 salariés franchi :** Obligations supplémentaires massives (Règlement intérieur obligatoire, accord de participation, versement transport, etc.).")

    st.markdown("---")
    st.warning("⚠️ **Rappel Juridique :** Les règles de calcul des seuils d'effectifs (Loi PACTE) et les obligations spécifiques peuvent varier selon votre Convention Collective. Faites valider votre situation par un conseiller juridique.")

# ------------------------------------------------------------------------------
# ONGLET 2 : SIMULATEUR DE COÛT D'EMBAUCHE
# ------------------------------------------------------------------------------
elif menu == "Simulateur de Coût d'Embauche":
    st.header("🧮 Simulateur de Coût d'Embauche Simplifié")
    st.write("Estimez le coût total d'un futur collaborateur avant de vous engager.")
    
    salaire_brut = st.number_input("Salaire mensuel Brut proposé (€) :", min_value=0, value=2200)
    
    # Calculs simplifiés basés sur les taux moyens en France
    charges_patronales_brutes = salaire_brut * 0.42
    
    # Simulation réduction générale de cotisations (Ex-Fillon) sous 1.6 SMIC (environ 2800€ brut)
    reduction_fillon = 0
    if salaire_brut < 2800:
        reduction_fillon = salaire_brut * 0.18
        
    frais_gestion = salaire_brut * 0.05
    salaire_net_estime = salaire_brut * 0.78
    cout_total_mensuel = salaire_brut + charges_patronales_brutes - reduction_fillon + frais_gestion
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Salaire NET Estimé (avant impôt)", f"{salaire_net_estime:,.2f} €")
        st.metric("Charges Patronales de base", f"{charges_patronales_brutes:,.2f} €")
    with col2:
        st.metric("Allégement de cotisations estimé", f"- {reduction_fillon:,.2f} €")
        st.metric("COÛT TOTAL MENSUEL POUR L'ENTREPRISE", f"{cout_total_mensuel:,.2f} €", delta_color="inverse")
        
    st.markdown("---")
    st.warning("⚠️ **Vigilance Légale :** Ce simulateur fournit une estimation basée sur les barèmes généraux du régime général de la Sécurité sociale. Il ne prend pas en compte les taux de prévoyance spécifiques à votre convention collective, les mutuelles d'entreprise, ni les exonérations géographiques particulières (ZRR, etc.). Une simulation de paie réelle doit être validée par votre expert-comptable.")

# ------------------------------------------------------------------------------
# ONGLET 3 : SUIVI DES CONGÉS & ABSENCES
# ------------------------------------------------------------------------------
elif menu == "Suivi des Congés & Absences":
    st.header("📅 Simulateur de Solde de Congés Payés")
    
    acquis = st.number_input("Nombre de jours de congés actuellement acquis par le salarié :", min_value=0.0, value=25.0, step=0.5)
    pris = st.number_input("Nombre de jours de congés demandés pour cette absence :", min_value=0.0, value=5.0, step=0.5)
    
    solde = acquis - pris
    
    if solde < 0:
        st.error(f"🚨 Alerte : Solde insuffisant ! Le salarié demande {pris} jours mais n'en dispose que de {acquis}. Solde négatif : {solde} jours.")
    else:
        st.success(f"✅ Demande validable. Solde restant après validation : **{solde} jours**.")
        
    st.subheader("💡 Rappel des Règles d'Or Légales :")
    st.markdown("* **Période principale :** Le salarié doit prendre au moins 12 jours continus entre le 1er mai et le 31 octobre.")
    st.markdown("* **Fractionnement :** Si le salarié prend une partie de son congé principal en dehors de cette période, cela peut lui ouvrir droit à des jours de fractionnement supplémentaires (sauf accord d'entreprise ou convention contraire).")
    st.markdown("* **Obligation de l'employeur :** Vous avez l'obligation de mettre vos salariés en mesure de prendre leurs congés. Le non-respect de cette règle engage votre responsabilité.")

# ------------------------------------------------------------------------------
# ONGLET 4 : TRAME D'ENTRETIEN ANNUEL
# ------------------------------------------------------------------------------
elif menu == "Trame d'Entretien Annuel":
    st.header("📝 Générateur de Trame d'Entretien Annuel d'Évaluation")
    st.write("Remplissez les champs ci-dessous pour générer un compte-rendu neutre et professionnel.")
    
    nom_salarie = st.text_input("Nom & Prénom du Salarié :", "Jean Dupont")
    poste = st.text_input("Poste occupé :", "Conseiller Clientèle")
    
    st.subheader("1. Bilan de l'année écoulée")
    reussites = st.text_area("Principales réussites et points forts professionnels :")
    axes_amelioration = st.text_area("Axes de progrès et compétences à développer :")
    
    st.subheader("2. Objectifs pour l'année à venir")
    objectifs = st.text_area("Objectifs professionnels (Fixer des critères mesurables et atteignables) :")
    
    texte_entretien = f"""COMPTE-RENDU D'ENTRETIEN ANNUEL D'ÉVALUATION
Entreprise : {nom_entreprise}
Salarié : {nom_salarie}
Poste : {poste}
--------------------------------------------------
1. BILAN DE L'ANNÉE ÉCOULÉE :
Réussites professionnelles : {reussites}
Axes d'amélioration professionnels : {axes_amelioration}

2. OBJECTIFS FUTURS :
{objectifs}

--------------------------------------------------
Fait à ........................., le .........................
