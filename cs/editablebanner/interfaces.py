from plone.theme.interfaces import IDefaultPloneLayer
from zope import schema
from zope.interface import Interface
from cs.editablebanner import EditableBannermessageFactory as _

class IProductLayer(Interface):
    """ Custom interface for our layer """

class IEditableBanner(Interface):
    """ The infterface for the editable footer """

    banner_text = schema.Text(title=_(u'Banner text'),
                              description=_(u'Insert here the HTML that will appear in the banner'),
                              required=False,
                              )
