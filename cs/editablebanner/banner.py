__version__ = '$Id: banner.py 12870 2008-07-14 08:16:42Z lur $'

from zope.component import adapts
from zope.interface import implements
from zope.formlib import form

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.layout.viewlets.common import ViewletBase

try:
    from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
    KUPU_WIDGET = True
except ImportError:
    KUPU_WIDGET = False



from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName

from cs.editablebanner import EditableBannermessageFactory as _
from cs.editablebanner.interfaces import IEditableBanner
class EditableBannerControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IEditableBanner)

    def __init__(self, context):
        super(EditableBannerControlPanelAdapter, self).__init__(context)
        self.portal = context
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.site_properties
        self.encoding = pprop.site_properties.default_charset
        self.fprops = pprop.banner_properties

    def get_banner_text(self):
	#import pdb;pdb.set_trace()
	language = self.portal.request.get('LANGUAGE', '')
	ida='banner_text_' + language
        text = getattr(self.fprops, ida, u'')
        return safe_unicode(text)
        
    def set_banner_text(self, value):
	#import pdb;pdb.set_trace()
	language = self.portal.request.get('LANGUAGE', '')
	ida='banner_text_' + language
	if value is not None:
	    value=value.encode(self.encoding)
	else:
	    value=''
	    
	if self.fprops.hasProperty(ida):
	    setattr(self.fprops, ida, value)
	else:
	    self.fprops.manage_addProperty(ida,value,'text')


    banner_text = property(get_banner_text, set_banner_text)



class EditableBannerControlPanel(ControlPanelForm):
    form_fields = form.FormFields(IEditableBanner)

    if KUPU_WIDGET:
        form_fields['banner_text'].custom_widget = WYSIWYGWidget

    form_name = _(u'Editable banner')
    label = _(u'Editable banner content')
    description = _(u'Enter the content of the banner')


class EditableBannerViewlet(ViewletBase):

    def update(self):
	#import pdb;pdb.set_trace()
	language = self.request.get('LANGUAGE', '')
	ida='banner_text_' + language
        pprops = getToolByName(self.context, 'portal_properties')
        fprops = pprops.banner_properties
        text = getattr(fprops, ida, u'')
        self.banner_text = safe_unicode(text)

    render = ViewPageTemplateFile('banner.pt')

    
    
