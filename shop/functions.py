#Helper functions
from elaphe import barcode
import Image, ImageDraw, ImageFont, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from saturnalia.settings import MEDIA_ROOT
import os

def make_ticket(ticket):
    '''Takes ticket or deposit object and generates the ticket PNG, saving to 
    model's ticket attribute.'''
    #Create the barcode and scale it up
    bc = barcode('ean13', '000000' + str(ticket.code), scale=5)
    #open the base ticket image
    ticket_png = Image.open(os.path.join(MEDIA_ROOT, 'tickets/base/ticket.png'))
    #paste the barcode into the bottom-right of the ticket
    paste_coords = (694, 2826)
    ticket_png.paste(bc, paste_coords)
    #Draw text onto ticket starting at the left, in line with the barcode
    draw = ImageDraw.Draw(ticket_png)
    font = ImageFont.truetype(os.path.join(MEDIA_ROOT, 'tickets/base/Anonymous.ttf'), 28)
    code_text = 'Ticket code: %s' %ticket.code
    name_text = 'Customer: %s' %ticket.order.fname + " " + ticket.order.lname
    draw.text((660,3250), code_text, fill="#333333", font=font)
    draw.text((660, 3300), name_text, fill="#333333", font=font)
    draw.text((1100,1300), str(ticket.code), fill="#333333", font=font)
    del draw
    #Save it off to the ticket's imagefield
    tf = StringIO.StringIO()
    ticket_png.save(tf, 'PNG')
    ticket_file = InMemoryUploadedFile(tf, None, 'ticket'+str(ticket.code)+'.png', 'image/jpeg', tf.len, None)
    ticket.ticket.save('ticket'+str(ticket.code)+'.png', ticket_file)
    del bc
    del ticket_png
    del font
    del tf
