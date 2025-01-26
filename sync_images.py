import os
import re
import shutil

# Percorsi
posts_dir = "/home/cox/Documents/sites/costidev/content/docs/"
attachments_dir = "/home/cox/Documents/costi/images/"
static_images_dir = "/home/cox/Documents/sites/costidev/static/images/"

# Estensioni di immagini supportate
supported_image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp")

# Step 1: Processa ogni file Markdown nella directory dei post
print("Inizio elaborazione dei file Markdown...")
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"Processando il file: {filename}")
        
        with open(filepath, "r") as file:
            content = file.read()
        
        # Step 2: Trova tutti i collegamenti alle immagini nel formato ![Image Description] oppure [[image.jpg]]
        images = re.findall(r'\[\[([^]]+\.(?:png|jpg|jpeg|gif|svg|bmp))\]\]', content, re.IGNORECASE)
        print(f"Immagini trovate nel file {filename}: {images}")
        
        # Step 3: Sostituisci i collegamenti alle immagini con un formato compatibile con Markdown
        for image in images:
            # Preparare il collegamento compatibile con Markdown
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            print(f"Collegamento sostituito: [[{image}]] -> {markdown_image}")
            
            # Step 4: Copia l'immagine nella directory static/images se esiste
            image_source = os.path.join(attachments_dir, image)
            image_destination = os.path.join(static_images_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, image_destination)
                print(f"Immagine copiata da {image_source} a {image_destination}")
            else:
                print(f"Attenzione: L'immagine {image_source} non esiste!")

        # Step 5: Scrivi il contenuto aggiornato nel file Markdown
        with open(filepath, "w") as file:
            file.write(content)
            print(f"Contenuto aggiornato scritto nel file: {filepath}")

print("Elaborazione completata.")
