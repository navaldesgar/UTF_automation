from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import os
import csv

# Lista de IDs de órdenes
order_ids = ["1674476029", "1674470932", "1674261260", "1674317877", "1674662078", "1674513183", "1674687112", "1674921326", "1674429810", "1673943905", "1674475202", "1674774569", "1674518154", "1674078706", "1674843794", "1674378805", "1674278386", "1674737049", "1674690023", "1674355393", "1674772235", "1674979334", "1674979176", "1674560278", "1674915877", "1674740826", "1674441163", "1674918085", "1674370221", "1674554532", "1674922917", "1674781306", "1674742640", "1674318453", "1674282000", "1674159399", "1674099745", "1674917418", "1674141337", "1674261664", "1674682636", "1674509232", "1674319074", "1674481794", "1674920819", "1674159925", "1674382010", "1674186878", "1674849212", "1674739372", "1674516849", "1674433500", "1674368496", "1674517938", "1674320995", "1674301858", "1674211294", "1674441354", "1674379736", "1674660025", "1674300561", "1674141688", "1674470718", "1674221309", "1674472284", "1674365720", "1674431603", "1674730841", "1674848645", "1674306146", "1674038165", "1674437588", "1674741003", "1674437175", "1674479338", "1674281147", "1674278942", "1674214480", "1674098568", "1674602652", "1674383107", "1674745001", "1674427936", "1674781827", "1674734109", "1674922589", "1674369257", "1674474229", "1674665033", "1674734590", "1674080192", "1674777908", "1674379733", "1673944946", "1674608475", "1673945504", "1674480064", "1674219201", "1674510785", "1674918802", "1674212969", "1674917387", "1674924781", "1674383130", "1674740771", "1674603149", "1674279541", "1675437732", "1675994613", "1675386271", "1675903888", "1675088053", "1675379645", "1675467404", "1675317941", "1675407953", "1675434757", "1675529035", "1675529536", "1675340248", "1675531357", "1675164454", "1675304635", "1675180625", "1675440916", "1675904361", "1675467095", "1675668603", "1675735299", "1675576511", "1675341556", "1675528199", "1675255856", "1675572383", "1675302144", "1675862289", "1675901884", "1675902827", "1675397826", "1675254298", "1675997522", "1675638025", "1675336323", "1675971970", "1675193984", "1675525059", "1675522931", "1675935835", "1675738156", "1675383864", "1675523537", "1675535375", "1675316307", "1675305175", "1675473374", "1675525300", "1675856380", "1675477242", "1675804514", "1675474445", "1675670929", "1675861595", "1675164147", "1675471401", "1676066358", "1675190731", "1675380408", "1675906086", "1675469242", "1675331939", "1675707034", "1675530204", "1675499423", "1675994606", "1675479182", "1675385238", "1675407115", "1675394696", "1675575484", "1675245796", "1675899215", "1675434445", "1675806571", "1675334410", "1675434987", "1675440203", "1675472037", "1675500663", "1675479998", "1675572252", "1675902536", "1675534882", "1675338189", "1675476943", "1675905802", "1675087879", "1675934989", "1675481344", "1675337784", "1675606030", "1675526657", "1675303678", "1675467664", "1675853232", "1675636960", "1676066485", "1675524190", "1675299068", "1675470341", "1675605491", "1675105875", "1675395675", "1675434860", "1675901004", "1675405509", "1675931952", "1675472084", "1675766793", "1675765163", "1675898576", "1675381390", "1675525348", "1675904751", "1675533124", "1675476195", "1675337159", "1675807718"]

# Carpeta donde se guardarán las imágenes
download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Proofs")
os.makedirs(download_dir, exist_ok=True)

# Configuración de Chrome
options = Options()
options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# Abrir login manual
driver.get("https://gt.us.logisticsbackoffice.com/dashboard/v2/hurrier/dashboard")
input("🔐 Inicia sesión y presiona ENTER aquí...")

# Lista para guardar órdenes sin imagen
ordenes_sin_imagen = []

# Procesar cada orden
for order_id in order_ids:
    print(f"⏳ Procesando orden {order_id}")
    url = f"https://gt.us.logisticsbackoffice.com/dashboard/v2/hurrier/order_details/{order_id}"
    driver.get(url)

    try:
        time.sleep(5)  # Esperar a que cargue la página

        # Intentar encontrar el enlace "Proof of return"
        link_element = driver.find_element(By.XPATH, "//a[contains(text(), 'Proof of return')]")
        image_url = link_element.get_attribute("href")

        # Descargar la imagen
        response = requests.get(image_url)
        if response.status_code == 200:
            file_path = os.path.join(download_dir, f"{order_id}.jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Imagen guardada: {file_path}")
        else:
            print(f"❌ No se pudo descargar imagen de {order_id}")
            ordenes_sin_imagen.append(order_id)

    except NoSuchElementException:
        # No hay botón "Proof of return", guardar orden
        ordenes_sin_imagen.append(order_id)
    except Exception as e:
        print(f"❌ Error inesperado en orden {order_id}: {e}")
        ordenes_sin_imagen.append(order_id)

driver.quit()
print("🎉 Proceso finalizado.")

# Guardar lista de órdenes sin imagen en CSV
csv_path = os.path.join(download_dir, "no_imagenes.csv")
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["orden_id"])
    for order_id in ordenes_sin_imagen:
        writer.writerow([order_id])

print(f"📄 CSV generado con órdenes sin imagen: {csv_path}")

