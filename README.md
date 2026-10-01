# SerieslyGR — αποθετήριο Kodi του Seriesly

Διεύθυνση (GitHub Pages): **https://hermesgr.github.io/SerieslyGR/**

## Α. Πρώτη φορά — ανέβασμα στο GitHub (μία φορά)
1. github.com → **New repository** → όνομα **SerieslyGR** → **Public** → Create.
2. **Add file → Upload files** → σύρε ΟΛΑ τα περιεχόμενα αυτού του φακέλου (μαζί με τους φακέλους
   `repo` και `νέα`, και το αρχείο `.nojekyll`) → **Commit changes**.
   (Στο κινητό το ανέβασμα φακέλων δεν δουλεύει — κάν' το από υπολογιστή.)
3. **Settings → Pages** → Source: **Deploy from a branch** → Branch: **main**, φάκελος **/ (root)** → **Save**.
4. Σε 1–2 λεπτά άνοιξε https://hermesgr.github.io/SerieslyGR/ — πρέπει να δεις «Seriesly για Kodi».

## Β. Εγκατάσταση σε κάθε Kodi (μία φορά ανά συσκευή)
1. **Ρυθμίσεις → Διαχείριση αρχείων → Προσθήκη πηγής** → `https://hermesgr.github.io/SerieslyGR/` → όνομα **Seriesly** → OK.
2. **Πρόσθετα → Εγκατάσταση από αρχείο zip** → **Seriesly** → `repository.seriesly-1.0.0.zip`.
3. **Πρόσθετα → Εγκατάσταση από αποθετήριο → Seriesly Repository → Πρόσθετα βίντεο → Seriesly → Εγκατάσταση**.
Από εκεί και πέρα οι ενημερώσεις έρχονται **αυτόματα** (το Kodi ελέγχει το αποθετήριο μόνο του).

## Γ. Κάθε νέα έκδοση του Seriesly
1. Βάλε το νέο zip (π.χ. `plugin.video.seriesly-1.0.2.zip`) στον φάκελο **νέα**.
2. Τρέξε `py build_repo.py` (δεξί κλικ σε κενό σημείο του φακέλου → «Άνοιγμα στο Τερματικό»).
3. Ανέβασε στο GitHub **τα αρχεία που γράφει στο τέλος** (Add file → Upload files, στους ίδιους φακέλους).
Σε λίγα λεπτά (το GitHub Pages ανανεώνεται σε ~1–10 λεπτά) κάθε Kodi βλέπει τη νέα έκδοση και ενημερώνεται.

## Περιεχόμενα
- `repository.seriesly-1.0.0.zip` — το πρόσθετο αποθετηρίου (αυτό εγκαθιστά ο χρήστης).
- `index.html` — η σελίδα που βλέπει η «πηγή» του Kodi.
- `repo/addons.xml`, `repo/addons.xml.md5` — ο κατάλογος που διαβάζει το Kodi για ενημερώσεις.
- `repo/zips/<πρόσθετο>/` — τα zip κάθε έκδοσης (+ εικονίδιο/φόντο).
- `build_repo.py` — ενημέρωση αποθετηρίου (μόνο Python, τίποτα για εγκατάσταση).
- `.nojekyll` — λέει στο GitHub Pages να σερβίρει τα αρχεία όπως είναι.
