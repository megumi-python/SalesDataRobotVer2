from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
import time
import os
#import shutil
from RPA.Archive import Archive

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    orders = get_orders()
    
    for row in orders:
        close_annoying_modal()
        #print("the contents of head:", row['Order number'])
        fill_the_form(row)
        preview_robot()
        submit_order(row)
        
        #break
    archive_receipts()


#########################################################

def open_robot_order_website():
    """Open the robot order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    time.sleep(1)

def get_orders():
    """Download the orders file, read it as a table, and return the result"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    tables = Tables()
    orders = tables.read_table_from_csv("orders.csv", header=True)
    return orders

def close_annoying_modal():
    """Close annoying modal: click OK"""
    page = browser.page()
    page.click("text=OK")
    time.sleep(1)

def fill_the_form(row):
    """Fill the form"""
    page = browser.page()
    page.select_option("#head",row['Head'])
    page.click(f"input[type='radio'][value='{row['Body']}']")
    page.fill("input[placeholder='Enter the part number for the legs']",row['Legs'])
    page.fill("#address",row['Address'])

def preview_robot():
    """Preview the robot"""
    page = browser.page()
    page.click("#preview")
    time.sleep(1)

def submit_order(row):
    """Submit the order"""
    page = browser.page()
    page.click("#order")
    
    max_attempt = 15
    for attempt in range(max_attempt):
        try:
            page.wait_for_selector("#order-another", timeout=5000)
            break
        except Exception as e:
            page.click("#order")
    
    pdf_path = store_receipt_as_pdf(str(row['Order number']))
    img_path = screenshot_robot(str(row['Order number']))
    embed_screenshot_to_receipt(img_path, pdf_path)
    
    page.click("#order-another")
    time.sleep(1)

def store_receipt_as_pdf(order_number):
    """Store the order receipt as a PDF file"""
    os.makedirs("output/receipts", exist_ok=True)
    pdf_path = "output/receipts/receipt_"+order_number+".pdf"
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(receipt_html, pdf_path)
    
    return pdf_path

def screenshot_robot(order_number):
    """Take a screenshot of the robot"""
    os.makedirs("output/images", exist_ok=True)
    img_path = "output/images/img_"+order_number+".png"
    page = browser.page()
    page.screenshot(path=img_path)
    
    return img_path

def embed_screenshot_to_receipt(screenshot, pdf_file):
   """Embed the robot screenshot to the receipt PDF file"""
   pdf = PDF()
   pdf.add_files_to_pdf(files=[screenshot], target_document=pdf_file, append=True)

#import shutil version
#def archive_receipts():
#   """Create a ZIP file of receipt PDF files"""
#   archive_path = shutil.make_archive("output_pdfs", "zip", "output/receipts", base_dir=".", verbose=0, dry_run=False)

#RPA.Archive version
def archive_receipts():
   """Create a ZIP file of receipt PDF files"""
   archive = Archive()
   archive.archive_folder_with_zip("output/receipts", "output/output_pdfs.zip")
