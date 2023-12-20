
from odoo.http import Controller, request, route
import base64


class HrEmployee(Controller):

    @route('/documents', type='http', auth='user',website = True)
    def get_hr_documents(self, **post):
        employee_id = request.env.user.employee_id
        if 'id' in post.keys():
            document_edit = request.env['res.document'].sudo().search(
                [('employee_id', "=", request.env.user.employee_id.id), ('id', '=', int(post['id']))])
        else:
            document_edit = False

        documents = request.env['res.document'].sudo().get_documents_table_in_portal(request.env.user.id)
        document_type = request.env['res.document.type'].sudo().search([])

        return request.render('tecfuge_hrms.portal_document_tree_view',{"documents":documents,'document_type':document_type,'employee':employee_id,'document_edit': document_edit})

    @route('/form/document_upload',type='http', auth='user',website = True,methods=['POST'],csrf=False)
    def document_submited_in_portal(self,**kwarg):
        documents = request.env['res.document'].sudo().create({'employee_id':request.env.user.employee_id.id})
        documents.document_type_id = int(kwarg['document_type_id'])
        documents.date_of_expire = kwarg['date_of_expire']
        document_file = kwarg['attachment_id']
        if document_file.filename:
            document_attachment = request.env['ir.attachment'].sudo().create({
                'name': document_file.filename,
                'datas': base64.encodebytes(document_file.read()),
                'type': 'binary',
                'public': True
            })
        documents.sudo().attachment_id = [document_attachment.id]

        print(documents)

        return request.redirect('/documents')

    @route('/delete/document',type='http', auth='user',website = True,csrf=False)
    def document_delete_in_portal(self,**kw):
        documents = request.env['res.document'].sudo().search([('employee_id',"=",request.env.user.employee_id.id),('id','=',int(kw['id']))])
        documents.sudo().unlink()
        return request.redirect('/documents')
    @route('/document/update',type='http', auth='user',methods=['POST'],website = True,csrf=False)
    def document_update_in_portal(self,**post):
        print("post",post)
        documents = request.env['res.document'].sudo().search([('employee_id',"=",request.env.user.employee_id.id),('id','=',int(post['id']))])
        documents.document_type_id = int(post['document_type_id'])
        documents.date_of_expire = post['date_of_expire']
        document_file=post['attachment_id']
        for rec in documents:
            rec.attachment_id.update({ 'name': document_file.filename,
                'datas': base64.encodebytes(document_file.read()),
                'type': 'binary',
                'public': True})
        # documents.sudo().unlink()
        return request.redirect('/documents')
