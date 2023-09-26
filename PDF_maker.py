from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# This fuction should return the fx rate from currency to NOK at invoice date. Currently hardcoded
def get_fx_rate(currency, date):
    # In the future this should talk to the Norges Bank fx rate API
    return {'EUR': 10, 'USD': 10.5}[currency]


def generate_context(customer, subsciption):

    total = 0
    for i in subsciption['product_table']:  # format numbers in product table

        subtotal = i[2]*i[4]*i[5]  # calculate subtotal
        total += subtotal
        i.append(subtotal)  # appending subtotal to line
        # formatting numbers with two decimals and thousands separation
        i[2] = f'{i[2]:,.2f}'.replace(',', ' ')
        i[4] = f'{i[4]:,.2f}'.replace(',', ' ')
        i[5] = f'{i[5]:,.2f}'.replace(',', ' ')
        i[6] = f'{i[6]:,.2f}'.replace(',', ' ')

    fx_rate = get_fx_rate(customer['currency'], subsciption['invoice_date'])

    subsciption['total'] = f'{total:,.2f}'.replace(
        ',', ' ')  # add total to dict
    # add total to dict
    subsciption['total_nok'] = f'{(total*fx_rate):,.2f}'.replace(',', ' ')

    # convert to HTML
    subsciption['product_table'] = ''.join(map(
        str, [f"<tr>{''.join([f'<th>{j}</th>' for j in i])}</tr>" for i in subsciption['product_table']]))

    subsciption['free_text'] = ''.join(
        map(str, [f'<p>{i}</p>' for i in subsciption['free_text']]))
    customer['address'] = ''.join(
        map(str, [f'<p>{i}</p>' for i in customer['address']]))

    # return one dictionary with all content
    return {**customer, **subsciption}


def create_invoice(invoice_data, filename="invoice.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # logo
    logo_path = "stock logo.jpeg"
    logo_width = width/2 - 50  # Adjust as needed
    logo_height = 100  # Adjust as needed
    margin = 50
    line_height = 12
    c.drawImage(logo_path, margin, height - logo_height,
                width=logo_width, height=logo_height)

    # Invoice Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0, 0, 0)  # Set text color to black
    c.drawString(width/2, height - margin, "INVOICE")

    # address field box
    box_width = width/2 - margin - 10
    box_height = (2+len(invoice_data['company_address']))*line_height
    box_x = margin
    box_y = height - margin - logo_height
    c.setFillColorRGB(0.8, 0.9, 1)  # Light blue color
    c.rect(box_x, box_y, box_width, box_height, fill=1, stroke=0)

    # address field text
    address_field_x = height - margin - logo_height + box_height
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)  # Set text color to black
    c.drawString(margin, address_field_x -
                 line_height, f'Customer ID: 10000001')
    c.setFont("Helvetica", 12)

    c.drawString(margin, address_field_x - 2*line_height,
                 invoice_data["company_name"])
    for i, x in enumerate(invoice_data['company_address']):
        c.drawString(margin, address_field_x - (3+i)*line_height,
                     x)

    # details field text
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)  # Set text color to black
    indent = 100
    c.drawString(width/2, address_field_x - line_height,
                 f'Invoice No.:')
    c.drawString(width/2, address_field_x - 2*line_height,
                 f'Invoice date:')
    c.drawString(width/2, address_field_x - 3*line_height,
                 f'delivery date:')
    c.drawString(width/2, address_field_x - 4*line_height,
                 f'Our reference:')
    c.drawString(width/2, address_field_x - 5*line_height,
                 f'Your reference:')

    c.drawString(width/2 + indent, address_field_x - line_height,
                 invoice_data["invoice_no"])
    c.drawString(width/2 + indent, address_field_x - 2 *
                 line_height, invoice_data["invoice_no"])
    c.drawString(width/2 + indent, address_field_x - 3 *
                 line_height, invoice_data["invoice_no"])
    c.drawString(width/2 + indent, address_field_x - 4 *
                 line_height, invoice_data["invoice_no"])
    c.drawString(width/2 + indent, address_field_x - 5 *
                 line_height, invoice_data["invoice_no"])

    # comment
    c.drawString(margin, address_field_x -
                 box_height - 2*line_height, invoice_data['comment'])

    # # Customer Information
    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(350, height - 100, "Bill To:")
    # c.setFont("Helvetica", 12)
    # c.drawString(350, height - 130, invoice_data["customer_name"])
    # c.drawString(350, height - 150, invoice_data["customer_address"])

    # # Invoice Details
    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(50, height - 200,
    #              f"Invoice Number: {invoice_data['invoice_number']}")
    # c.drawString(50, height - 230, f"Date: {invoice_data['date']}")

    # Table Headers
    y_position = height - 300
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Item")
    c.drawString(250, y_position, "Description")
    c.drawString(400, y_position, "Quantity")
    c.drawString(480, y_position, "Price")
    c.drawString(550, y_position, "Total")

    # Table Data
    y_position -= 30
    c.setFont("Helvetica", 12)
    for item in invoice_data["items"]:
        c.drawString(50, y_position, item["name"])
        c.drawString(250, y_position, item["description"])
        c.drawString(400, y_position, str(item["quantity"]))
        c.drawString(480, y_position, f"${item['price']:.2f}")
        c.drawString(550, y_position, f"${item['total']:.2f}")
        y_position -= 30

    # Total Amount
    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, y_position - 30, "Total Amount:")
    c.drawString(550, y_position - 30, f"${invoice_data['total_amount']:.2f}")

    c.save()


def main():
    # for testing purposes
    invoice_data = {
        'company_id': '100001',
        'company_name': 'Tech Corp.',
        'company_address': ["123 Tech St", "Tech City", "12345", "USA"],
        'invoice_no': '950',
        'comment': 'Some license for some stuff',
        "items": [
            {"name": "Item1", "description": "Some tech item",
             "quantity": 2, "price": 50.00, "total": 100.00},
            {"name": "Item2", "description": "Another tech item",
             "quantity": 1, "price": 150.00, "total": 150.00},
        ],
        "total_amount": 250.00
    }

    create_invoice(invoice_data)


if __name__ == "__main__":
    main()
