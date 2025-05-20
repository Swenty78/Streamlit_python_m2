import pandas as pd
from pyquery import PyQuery as pq
import requests


website_response = requests.get("https://www.leportagesalarial.com/coworking/")
all_urls = []
all_coworking_data = []
if website_response.status_code == 200:
  html_content = website_response.text
  parsed_html = pq(html_content)

  # Find the <h3> tag and select the next sibling <ul>
  target_ul = parsed_html('h3:contains("Coworking Paris – Île de France :") + ul')

  # Extract URLs from <li> elements within target_ul
  for list_item in target_ul.find('li').items():
      link_element = list_item.find('a')
      if link_element:
          all_urls.append(link_element.attr('href'))


for url in all_urls :
  page_response = requests.get(url)

  coworking_data = {}  # Dictionary for the current URL's data



  if page_response.status_code == 200:
      page_content = page_response.text
      page_parsed = pq(page_content)

      # Extract coworking space name
      h2_element = page_parsed('h2:contains("Contacter")')
      coworking_space_name = h2_element.text().replace("Contacter", "").strip()
      coworking_data['nom'] = coworking_space_name

      contact_ul = page_parsed('h2:contains("Contacter") + ul')

      for list_item in contact_ul.find('li').items():
          text = list_item.text()
          link_element = list_item.find('a')

          # Extract and store data based on keywords
          if "Adresse :" in text:
              coworking_data['adresse'] = text.replace("Adresse :", "").strip()
          elif "Téléphone :" in text:
              coworking_data['téléphone'] = text.replace("Téléphone :", "").strip()
          elif "Accès :" in text:
              coworking_data['Accès'] = text.replace("Accès :", "").strip()
          elif "Site :" in text and link_element:
              coworking_data['Site'] = link_element.attr('href')
          elif "Instagram :" in text and link_element:
              coworking_data['Instagram'] = link_element.attr('href')
          elif "Google plus :" in text and link_element:
              coworking_data['Google plus'] = link_element.attr('href')


      all_coworking_data.append(coworking_data)  # Append dictionary to the list
  else:
        print(f"Error connecting to: {url} - Status code: {page_response.status_code}")

# Exporter les données vers un fichier CSV
output_file = 'coworking_data_pandas.csv'

# Créer un DataFrame pandas à partir de la liste de dictionnaires
if all_coworking_data:
    df = pd.DataFrame(all_coworking_data)
    # Exporter le DataFrame en CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Les données ont été exportées dans le fichier {output_file}.")
else:
    print("La liste des données de coworking est vide, aucun fichier n'a été généré.")