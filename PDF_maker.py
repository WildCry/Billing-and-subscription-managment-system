import jinja2
import pdfkit
from datetime import date
import os

def get_fx_rate(currency, date): # This fuction should return the fx rate from currency to NOK at invoice date. Currently hardcoded
    return {'EUR': 10, 'USD': 10.5}[currency] # In the future this should talk to the Norges Bank fx rate API

def generate_context(customer, subsciption):

    total = 0
    for i in subsciption['product_table']: # format numbers in product table

        subtotal = i[2]*i[4]*i[5] # calculate subtotal
        total += subtotal
        i.append(subtotal) # appending subtotal to line
        i[2] = f'{i[2]:,.2f}'.replace(',', ' ') # formatting numbers with two decimals and thousands separation
        i[4] = f'{i[4]:,.2f}'.replace(',', ' ')
        i[5] = f'{i[5]:,.2f}'.replace(',', ' ')
        i[6] = f'{i[6]:,.2f}'.replace(',', ' ')
    
    fx_rate = get_fx_rate(customer['currency'], subsciption['invoice_date'])
    
    subsciption['total'] = f'{total:,.2f}'.replace(',', ' ') # add total to dict
    subsciption['total_nok'] = f'{(total*fx_rate):,.2f}'.replace(',', ' ') # add total to dict

    # convert to HTML
    subsciption['product_table'] = ''.join(map(str,[f"<tr>{''.join([f'<th>{j}</th>' for j in i])}</tr>" for i in subsciption['product_table']]))

    subsciption['free_text'] = ''.join(map(str,[f'<p>{i}</p>' for i in subsciption['free_text']]))
    customer['address'] = ''.join(map(str,[f'<p>{i}</p>' for i in customer['address']]))
 
    return {**customer, **subsciption} # return one dictionary with all content

def create_invoice(customer, subsciption):
    
    context = generate_context(customer, subsciption)
    
    template_name = 'invoice_template.html'
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print('current dir:', current_dir)
    template_path = os.path.join(current_dir, template_name)
    print('template_path',template_path)
    template_path = os.path.join(current_dir, 'logo.jpg')
    print(template_path,template_path)
    context['logo'] = template_path
    print(context)
    template_loader = jinja2.FileSystemLoader(os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader)

    html_template = template_name
    template = template_env.get_template(html_template)
    output_text = template.render(context)
    
    print(output_text)
    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output_pdf = os.path.join(current_dir, f'invoice {subsciption["invoice_no"]}.pdf')
    print('ouput', output_pdf)
    
    css_path = os.path.join(current_dir, 'style.css')
    print('css_path',css_path)
    
    pdfkit.from_string(output_text, output_pdf, configuration=config, css=css_path, options={"enable-local-file-access": ""})
    
def main():
    # These dictionaries are for testing Only
    subsciption = {'customer_id': 100007,
                'invoice_date': date(2023,2,6),
                'due_date': date(2023,7,2),
                'comment': 'Aultman Healthcare - Mazemap establishment and license 2023',
                'product_table': [[2, 'MazeMap establishemnt', 1,'', 40395, 0.5],
                                    [4, 'MazeMap license', 1,'', 46292, 0.5]],
                'free_text': ['Mazemap establishment (AG Insurance 1223 sqm)',
                                'Mazemap establishment (Polydigital 4945 sqm)',
                                'MazeMap license 2023-07-1 : 2024-06-31 (12 months)',
                                'Effective 1st July 2023, if the accumulated nr of sqm is less than 0.2 million sqm, then the license effective from 1st July 2023 is calculated based on 0.2 million sqm of maps'],
                'invoice_no': 920, # This should be changed
                'our_reference': 'John Doe',
                'their_reference': 'Jane Smith',
                }

    customer = {'customer_id': 100007,
                'name': 'PLANIT', 
                'address': ['7792 Olentangy River Road','Columbus','43235','USA'], 
                'currency': 'EUR',
                }
    
    create_invoice(customer, subsciption)

if __name__ == "__main__":
    main()