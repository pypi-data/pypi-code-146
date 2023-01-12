from django.http import FileResponse
import os
import shutil
from django import http
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.shortcuts import render

from .operations.location import LocationOperations
from .operations.explorer import ExplorerOperations

class Explorer(TemplateView):
    template_name = 'explorer/index.html'
    http_method_names = ['get', 'post']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        return None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return http.HttpResponseRedirect(f'/admin/login/?next={reverse("explorer-main")}')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # GETTING OPERATION OBJECT
        xo = ExplorerOperations(request)

        # PERFORMING VALIDATION
        if not xo.isValid():
            return self._render_warning(request, xo.getMessage())

        # GETTING VOLUME AND PATH INFORMATION
        volume_info, location_path = xo.getVolumeInfo(), xo.getLocationPath()
        if xo.getMessage():
            return self._render_warning(request, xo.getMessage())

        # GETTING LOCATION OBJECT
        lo = LocationOperations(volume_info, location_path)

        # IS LOCATION IS FILE
        if lo.isLocationFile():
            return self._render_file(request, lo.getLocationPath())

        # GETTING LOATION REATED DATA
        data_list = lo.getData() # Getting location file and dir data.
        summary_data = lo.getDataSummary() # Getting summary data.
        navigation_bar_data = lo.getNavigationBarData() # Getting navigation bar data.

        # GETTING EXPLORER RELATED DATA
        page_data = xo.getPageData(data_list) # Getting page data.
        pagination_data = xo.getPaginationData(page_data) # Getting pagination data.
        
        # MAKING CONTEXT 
        context = self.get_context_data()
        context.update({
            'volume_data': xo.getVolumeData(),
            'action_data': xo.getActionData(),
            'summary_data': summary_data,
            'navigation_bar_data': navigation_bar_data,
            'page_data': page_data,
            'pagination_data': pagination_data
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # GETTING OPERATION OBJECT
        xo = ExplorerOperations(request)

        # PERFORMING VALIDATION
        if not xo.isValid():
            return self._render_warning(request, xo.getMessage())

        # GETTING VOLUME AND PATH INFORMATION
        volume_info, location_path = xo.getVolumeInfo(), xo.getLocationPath()
        if xo.getMessage():
            return self._render_warning(request, xo.getMessage())

        # GETTING LOCATION OBJECT
        lo = LocationOperations(volume_info, location_path)

        # GETTING LOATION REATED DATA
        data_list = lo.getData() # Getting location file and dir data.
        path_list = xo.getCheckedFilePath(data_list) # Getting page data.

        # PERFORMING ACTION
        file_path = lo.performAction(path_list, xo.getAction())

        if file_path: # Download case
            return FileResponse(open(file_path, 'rb'), as_attachment=True)

        return self._redirect_to_same(request)

    def render_to_response(self, context, **response_kwargs) -> http.HttpResponse:
        
        return super().render_to_response(context, **response_kwargs)

    def _redirect_to_same(self, request):
        """Redirect to same url."""
        return http.HttpResponseRedirect(request.get_full_path())

    def _render_warning(self, request, message):
        """Rendered warning template"""
        return render(request, 'explorer/warning.html', {'message': message})

    def _render_file(self, request, file_path):
        """Return the file render response."""
        return FileResponse(open(file_path, 'rb'), as_attachment=False)