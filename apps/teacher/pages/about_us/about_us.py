import streamlit as st
from apps.teacher.reset_apps import reset_apps

## Setzt bei Page-Wechsel alles zurück
# Wenn er davor nicht auf der Seite war, App zurücksetzen
if st.session_state.current_page != "apps/teacher/pages/about_us/about_us.py":    
  reset_apps()
  # Außerdem Seite, auf derzeitige Seite setzen
  st.session_state.current_page = "apps/teacher/pages/about_us/about_us.py"

st.title("Über uns 👥")

st.subheader("Bevor wir von uns erzählen kurz zu dir!", divider="blue", anchor=False)

st.write("Zu mir?!")
st.write("**Ja zu dir - weil - du verdammt wichtig bist.**")
st.write("Auch wenn du dir das wahrscheinlich viel zu selten eingestehst...")

st.write('''Du bist nicht einfach nur Lehrer geworden, wegen 9 Wochen Sommerferien und weil du "am Dienstag zu Mittag" aus haben möchtest. Aber Spaß beiseite ;-)
         \n\n Du bist LehrerIn geworden, weil du etwas verändern wolltest. Weil du die Welt zumindest um 1% besser machen wolltest...
         \n\n Mittlerweile bist du schon mehrere Jahre LehrerIn und die Routine hat eingesetzt: Die SchülerInnen werden anstrengender, die Verantwortungen größer und du fühlst dich öfters ausgelaugt und erschöpft.
         \n\n Es ist so als wäre das System einfach so geschaffen, dass vieles so anstrengend ist.
         \n\n Du bist manchmal frustriert. Das ist okay. Wir sind auch manchmal frustriert. Vor allem dann, wenn ich glaube alles gegeben zu haben und es fruchtet einfach nicht. Es fruchtet !noch! nicht.''')

st.write('''Ich möchte dir jetzt nicht versprechen, dass wir alle Probleme lösen können. Können wir leider auch nicht und werden wir wahrscheinlich nie können - aber wir möchten dir den Kopf zumindest ein wenig freispielen, dass du wieder die Ressourcen hast, die Schülerin und den Schüler in den Vordergrund zu stellen. Der Grund, warum du eigentlich LehrerIn geworden bist.
         \n\n Zumindest hast du dir bei deiner Entscheidung gedacht, dass du es um mindestens 10% besser machen kannst, als die Lehrer, die du hattest.''')

st.write("Und jetzt mal Hand aufs Herz: Die Gesellschaft schaut auf auf Ärzte, Rechtsanwälte und vielleicht Universitätsprofessoren, aber du bist mindestens genau so wichtig für unser Land, unsere Gesellschaft, unsere Welt und unsere Zukunft.")

st.write("Deshalb danke, vielen Dank, dass du tust, was du tust. Auch wenn es schwierig ist, wenn es anstrengend ist und wenn du nicht einmal im geringsten die Anerkennung bekommst, die du eigentlich dafür verdienst.")

st.write("Denke ich mir das jeden Tag beim Unterrichten in der Klasse selbst? Nein, absolut nicht. Aber es hilft mir in Erinnerung zu rufen, dass ich mit meiner Zeit etwas verdammt Sinnvolles mache, auch wenn es sich so extrem oft nicht danach anfühlt.")

st.write("Mach weiter deinen Job so gut du kannst und wir versuchen dir mit ein paar coolen Tools zumindest ein wenig Arbeit abzunehmen.")

st.write("Liebe Grüße,")

st.write("dein Daniel und dein Philipp")

st.write("Lehrer an einer HLW und Lehrer an einer FMS in Österreich")
