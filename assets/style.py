def return_styles():
  styles = '''

  #MainMenu {visibility: hidden;}

  footer {visibility: hidden;}

  #stDecoration {display: none;}

  .stAppToolbar {display: none;}

  .stButton:focus {color: white !important; }

  .c-h1 {
    font-size: 2.8rem; 
    font-weight: 600;
    text-align: left;
    /* hilft nicht
    padding: 0;
    margin: 0; */
  }

  /* Tablet */
  @media (max-width: 768px) {
    .c-h1 {
      font-size: 2rem;  /* 36px */
    }
  }

  /* Smartphone */
  @media (max-width: 480px) {
    .c-h1 {
      font-size: 1.5rem;  /* 24px */
    }
  }

  button[data-testid="stBaseButton-secondary"] {
  background-color: #60a5fa;
  color: white;
  border: none !important;
  box-shadow: none !important;
}

button[data-testid="stBaseButton-secondary"]:hover {
  background-color: #3b82f6;
  color: white;
}

button[data-testid="stBaseButton-secondary"]:active {
  background-color: #93c5fd;
}

button[data-testid="stBaseButton-secondary"]:focus p {
    color: white; 
  }    

  a[href="https://streamlit.io/cloud"] {
    display: none !important;
  }

  a[href="https://share.streamlit.io/user/philipp-schrittwieser"] {
    display: none !important;
  }
  
  ._link_gzau3_10 {
    display: none !important;
  }

  ._profileContainer_gzau3_53 {
    display: none !important;
  }

  img[data-testid="stLogo"] {
        height: 5rem;  /* Ändern Sie die Höhe nach Bedarf */
        width: auto;    /* Automatische Breite, um das Seitenverhältnis beizubehalten */
        border-radius: 5%;
    }
  '''
  return styles