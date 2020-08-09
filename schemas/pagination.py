from flask import request
from marshmallow import Schema,fields
from urllib.parse import urlencode


class PaginationSchema(Schema):
    class Meta:
        ordered = True

    # PaginationSchema inherits from marshmallow.Schema
    # PaginationSchema is used to serialize the pagination object from Flask-SQL Alchemy.
    # The links atttribute is a custom field, which means
    # that we can specify how we are going to seriealize it
    links = fields.Method(serialize ='get_pagination_links')
    page = fields.Integer(dump_only = True)
    pages = fields.Integer(dump_only = True)
    per_page = fields.Integer(dump_only = True)
    total = fields.Integer(dump_only = True)

    @staticmethod
    def get_url(page):
        """
        This method is used to generate the URL of the page based
        on the page number. It is taking in the page number parameter and
        adding that to the request arguments dictionairy. Finally, it encodes
        and returns the new URL, including the page number, as an argument.
        """
        query_args = request.args.to_dict()
        query_args['page'] = page
        return f'{request.base_url}?{urlencode(query_args)}'

    def get_pagination_links(self,paginated_objects):
        """
        This method is used to generate URL links to different pages.
        It gets the page's information from paginated_objects and relies
        on the get_url method.

        :param paginated_objects:
        :return:
        """
        pagination_links = {
            'first':self.get_url(page = 1),
            'last': self.get_url(page = paginated_objects.pages)
        }

        if paginated_objects.has_prev:
            pagination_links['prev'] = self.get_url(page = paginated_objects.prev_num)
        if paginated_objects.has_next:
            pagination_links['next'] = self.get_url(page = paginated_objects.next_num)
        return pagination_links