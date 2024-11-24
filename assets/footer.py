import streamlit as st

def footer():
    footer_html = """
    <style>
    .stAppHeader {
        display: none;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #4b5563;
        text-align: center;
        padding: 0px 0px 5px 0px;
        font-size: 0.8rem;  /* 14px/16 */
    }
    .modal-trigger {
        display: none;
    }
    .modal {
        display: none;
        position: fixed;
        z-index: 999991;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        overflow: auto;
    }
    .modal-content {
        padding: 1.25rem;  /* 20px/16 */
        border-radius: 0.625rem;  /* 10px/16 */
        border: 1px solid #888;
        background-color: white;
        margin: 10% auto;
        width: 80%;
        max-width: 62.5rem;  /* 1000px/16 */
    }
    .modal-trigger:checked + .modal {
        display: block;
    }
    .close-btn {
        font-size: 2.5rem;  /* 40px/16 */
        float: right;
        cursor: pointer;
    }
    </style>

    <div class="footer">
        <span>© AI School 2024</span>
        <label for="impressum-trigger" style="margin: 0 0.7rem; cursor: pointer;">Impressum</label>
        <label for="datenschutz-trigger" style="cursor: pointer;">Datenschutz</label>
    </div>
    """

    modal1 = """
    <input type="checkbox" id="impressum-trigger" class="modal-trigger">
    <div class="modal">
        <div class="modal-content">
            <label for="impressum-trigger" class="close-btn">&times;</label>
            <h2>Impressum</h2>
            <p>Angaben gemäß § 5 TMG</p>
            <address>
                Philipp Schrittwieser, BSc, MBA<br>
                Schrittwieser AI Technologies e.U.<br>
                Fasangartengasse 5-7/1/1<br>
                1130 Wien
            </address>
            <h2>Kontakt</h2>
            <p>
                Telefon: (+43) 0676 / 782 11 31<br>
                E-Mail: <a href="mailto:schrittwieser@aitechnologies.at">schrittwieser@aitechnologies.at</a>
            </p>
            <h2>Umsatzsteuer-ID</h2>
            <p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: ATU79754678</p>
            <h2>Berufsbezeichnung und berufsrechtliche Regelungen</h2>
            <p>
                Berufsbezeichnung: Dienstleistungen in der automatischen Datenverarbeitung und Informationstechnik<br>
                Zuständige Kammer: Wirtschaftskammer Österreich (WKO)<br>
                Verliehen in: Österreich<br>
                Es gelten folgende berufsrechtliche Regelungen:
            </p>
            <h2>EU-Streitschlichtung</h2>
            <p>
                Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit:
                <a href="https://ec.europa.eu/consumers/odr/">https://ec.europa.eu/consumers/odr/</a>.<br>
                Unsere E-Mail-Adresse finden Sie oben im Impressum.
            </p>
            <h2>Verbraucherstreitbeilegung/Universalschlichtungsstelle</h2>
            <p>
                Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.
            </p>
            <p>Quelle: <a href="https://www.e-recht24.de">www.e-recht24.de</a></p>
        </div>
    </div>
    """

    modal2 = """
    <input type="checkbox" id="datenschutz-trigger" class="modal-trigger">
    <div class="modal">
        <div class="modal-content">
            <label for="datenschutz-trigger" class="close-btn">&times;</label>
            <h2>Datenschutzerklärung</h2>
            <h4>Allgemeine Hinweise</h4>
            <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können. Ausführliche Informationen zum Thema Datenschutz entnehmen Sie unserer unter diesem Text aufgeführten Datenschutzerklärung.</p>
            <h4>Datenerfassung auf dieser Website</h4>
            <p><strong>Wer ist verantwortlich für die Datenerfassung auf dieser Website?</strong></p>
            <p>Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen Kontaktdaten können Sie dem Abschnitt „Hinweis zur Verantwortlichen Stelle" in dieser Datenschutzerklärung entnehmen.</p>
            <p><strong>Wie erfassen wir Ihre Daten?</strong></p>
            <p>Ihre Daten werden zum einen dadurch erhoben, dass Sie uns diese mitteilen. Hierbei kann es sich z. B. um Daten handeln, die Sie in ein Kontaktformular eingeben.</p>
            <p>Andere Daten werden automatisch oder nach Ihrer Einwilligung beim Besuch der Website durch unsere IT-Systeme erfasst. Das sind vor allem technische Daten (z. B. Internetbrowser, Betriebssystem oder Uhrzeit des Seitenaufrufs). Die Erfassung dieser Daten erfolgt automatisch, sobald Sie diese Website betreten.</p>
            <p><strong>Wofür nutzen wir Ihre Daten?</strong></p>
            <p>Ein Teil der Daten wird erhoben, um eine fehlerfreie Bereitstellung der Website zu gewährleisten. Andere Daten können zur Analyse Ihres Nutzerverhaltens verwendet werden.</p>
            <p><strong>Welche Rechte haben Sie bezüglich Ihrer Daten?</strong></p>
            <p>Sie haben jederzeit das Recht, unentgeltlich Auskunft über Herkunft, Empfänger und Zweck Ihrer gespeicherten personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die Berichtigung oder Löschung dieser Daten zu verlangen. Wenn Sie eine Einwilligung zur Datenverarbeitung erteilt haben, können Sie diese Einwilligung jederzeit für die Zukunft widerrufen. Außerdem haben Sie das Recht, unter bestimmten Umständen die Einschränkung der Verarbeitung Ihrer personenbezogenen Daten zu verlangen. Des Weiteren steht Ihnen ein Beschwerderecht bei der zuständigen Aufsichtsbehörde zu.</p>
            <h3>Hosting</h3>
            <h4>Externes Hosting</h4>
            <p>Diese Website wird extern gehostet. Die personenbezogenen Daten, die auf dieser Website erfasst werden, werden auf den Servern des Hosters gespeichert. Hierbei kann es sich v. a. um IP-Adressen, Kontaktanfragen, Meta- und Kommunikationsdaten, Vertragsdaten, Kontaktdaten, Namen, Websitezugriffe und sonstige Daten, die über eine Website generiert werden, handeln.</p>
            <p>Das externe Hosting erfolgt zum Zwecke der Vertragserfüllung gegenüber unseren potenziellen und bestehenden Kunden (Art. 6 Abs. 1 lit. b DSGVO) und im Interesse einer sicheren, schnellen und effizienten Bereitstellung unseres Online-Angebots durch einen professionellen Anbieter (Art. 6 Abs. 1 lit. f DSGVO).</p>
            <p>Wir setzen folgende(n) Hoster ein:</p>
            <p>Vercel</p>
            <h3>Allgemeine Hinweise und Pflichtinformationen</h3>
            <h4>Datenschutz</h4>
            <p>Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend den gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.</p>
            <h4>Hinweis zur verantwortlichen Stelle</h4>
            <p>Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:</p>
            <p>
                Schrittwieser AI Technologies e.U.<br>
                Philipp Schrittwieser, BSc, MBA<br>
                Fasangartengasse 5-7<br>
                1130 Wien<br>
                Österreich
            </p>
            <p>
                Telefon: +43 (0) 676 782 11 31<br>
                E-Mail: schrittwieser@aitechnologies.at
            </p>
            <p>Quelle: <a href="https://www.e-recht24.de">www.e-recht24.de</a></p>
        </div>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)
    st.markdown(modal1, unsafe_allow_html=True)
    st.markdown(modal2, unsafe_allow_html=True)
