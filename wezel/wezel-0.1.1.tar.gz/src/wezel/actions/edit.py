import numpy as np
import dbdicom as db
import wezel


def all(parent):

    parent.action(DeleteSeries, text='Series > Delete')
    parent.action(Copy, text='Series > Copy', generation=3)
    parent.action(CopySeries, text='Series > Copy to..')
    parent.action(MoveSeries, text='Series > Move to..')
    parent.action(MergeSeries, text='Series > Merge')
    parent.action(GroupSeries, text='Series > Group')
    parent.action(SeriesRename, text='Series > Rename')
    parent.action(SeriesExtractByIndex, text='Series > Extract subseries (by index)')
    parent.action(SeriesExtractByValue, text='Series > Extract subseries (by value)')
    parent.separator()
    parent.action(DeleteStudies, text='Studies > Delete')
    parent.action(Copy, text='Studies > Copy', generation=2)
    parent.action(CopyStudies, text='Studies > Copy to..')
    parent.action(MoveStudies, text='Studies > Move to..')
    parent.action(MergeStudies, text='Studies > Merge')
    parent.action(GroupStudies, text='Studies > Group')
    parent.action(StudiesRename, text='Studies > Rename')
    parent.action(NewSeries, text='Studies > New series')
    parent.separator()
    parent.action(Delete, text='Patients > Delete', generation=1)
    parent.action(Copy, text='Patients > Copy', generation=1)
    parent.action(MergePatients, text='Patients > Merge')
    parent.action(PatientsRename, text='Patients > Rename')
    parent.action(NewStudy, text='Patients > New study')
    parent.separator()
    parent.action(NewPatient, text='Database > New patient')
    

class Copy(wezel.Action):

    def enable(self, app):
        return app.nr_selected(self.generation) != 0

    def run(self, app):

        app.status.message("Copying..")
        records = app.get_selected(self.generation)   
        # This can be faster - copy all in one go     
        for j, record in enumerate(records):
            #app.status.progress(j, len(records), 'Copying..')
            record.copy()               
        app.refresh()


class Delete(wezel.Action):

    def enable(self, app):
        return app.nr_selected(self.generation) != 0

    def run(self, app):
        app.status.message("Deleting..")
        records = app.get_selected(self.generation)        
        for j, record in enumerate(records):
            app.status.progress(j, len(records), 'Deleting..')
            record.remove()
        app.refresh()


class DeleteSeries(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        series = app.selected('Series')        
        for j, sery in enumerate(series):
            app.status.progress(j, len(series), 'Deleting..')
            sery.remove()
        app.refresh()

class DeleteStudies(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app):
        studies = app.selected('Studies')        
        for j, study in enumerate(studies):
            app.status.progress(j, len(studies), 'Deleting..')
            study.remove()
        app.refresh()

class CopySeries(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        studies = app.folder.studies()
        labels = [s.label() for s in studies]
        cancel, f = app.dialog.input(
            {'type':'dropdownlist', 'label':'Copy to study: ', 'list': labels, 'value': 0},
            title = 'Copy to which study?')
        if cancel:
            return
        study = studies[f[0]['value']]
        series = app.selected('Series')        
        for j, sery in enumerate(series):
            app.status.progress(j, len(series), 'Moving..')
            sery.copy_to(study)               
        app.refresh()


class MoveSeries(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        studies = app.folder.studies()
        labels = [s.label() for s in studies]
        cancel, f = app.dialog.input(
            {'type':'dropdownlist', 'label':'Move to study: ', 'list': labels, 'value': 0},
            title = 'Move to which study?')
        if cancel:
            return
        study = studies[f[0]['value']]
        series = app.selected('Series')        
        for j, sery in enumerate(series):
            app.status.progress(j, len(series), 'Moving..')
            sery.move_to(study)               
        app.refresh()


class MoveStudies(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app):
        patients = app.folder.patients()
        labels = [p.label() for p in patients]
        cancel, f = app.dialog.input(
            {'type':'dropdownlist', 'label':'Move to patient: ', 'list': labels, 'value': 0},
            title = 'Move to which patient?')
        if cancel:
            return
        patient = patients[f[0]['value']]
        studies = app.selected('Studies')        
        for j, study in enumerate(studies):
            app.status.progress(j, len(studies), 'Moving..')
            study.move_to(patient)               
        app.refresh()


class CopyStudies(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app):
        patients = app.folder.patients()
        labels = [p.label() for p in patients]
        cancel, f = app.dialog.input(
            {'type':'dropdownlist', 'label':'Copy to patient: ', 'list': labels, 'value': 0},
            title = 'Copy to which patient?')
        if cancel:
            return
        patient = patients[f[0]['value']]
        studies = app.selected('Studies')
        for j, study in enumerate(studies):
            app.status.progress(j, len(studies), 'Copying..')
            study.copy_to(patient)
        app.refresh()


class NewSeries(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        app.status.message('Creating new series..')
        studies = app.selected('Studies')
        for study in studies:
            study.new_series(SeriesDescription='New series')
        app.refresh()


class NewStudy(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Patients') != 0

    def run(self, app): 
        app.status.message('Creating new study..')
        patients = app.selected('Patients')
        for patient in patients:
            patient.new_study(StudyDescription='New study')
        app.refresh()


class NewPatient(wezel.Action):

    def enable(self, app):
        return True

    def run(self, app): 
        app.status.message('Creating new patient..')
        app.folder.new_patient(PatientName='New patient')
        app.refresh()


class MergeSeries(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app): 

        app.status.message('Merging..')
        records = app.selected('Series')
        #study = records[0].new_pibling(StudyDescription='Merger')
        study = records[0].parent()
        series = study.new_series(SeriesDescription='Merged series')
        db.merge(records, series)
        app.refresh()


class MergeStudies(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        app.status.message('Merging..')
        studies = app.selected('Studies')
        patient = studies[0].new_pibling(PatientName='Merger')
        db.merge(studies, patient.new_study(StudyDescription='Merged studies'))
        app.refresh()

class MergePatients(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Patients') != 0

    def run(self, app): 
        app.status.message('Merging..')
        records = app.selected('Patients')
        patient = records[0].new_sibling(PatientName='Merged Patients')
        db.merge(records, patient)
        app.refresh()


class GroupSeries(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app): 
        app.status.message('Grouping..')
        records = app.selected('Series')
        study = records[0].new_pibling(StudyDescription='Grouped')
        db.group(records, study)
        app.status.hide()
        app.refresh()

class GroupStudies(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        app.status.message('Grouping..')
        records = app.selected('Studies')
        patient = records[0].new_pibling(PatientName='Grouped')
        db.group(records, patient)
        app.status.hide()
        app.refresh()


class SeriesRename(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app): 
        series_list = app.get_selected(3)
        for s in series_list:
            cancel, f = app.dialog.input(
                {"type":"string", "label":"New series name:", "value": s.SeriesDescription},
                title = 'Enter new series name')
            if cancel:
                return
            s.SeriesDescription = f[0]['value']
        app.refresh()


class StudiesRename(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Studies') != 0

    def run(self, app): 
        for s in app.selected('Studies'):
            cancel, f = app.dialog.input(
                {"type":"string", "label":"New study name:", "value": s.StudyDescription},
                title = 'Enter new study name')
            if cancel:
                return
            s.StudyDescription = f[0]['value']
        app.refresh()


class PatientsRename(wezel.Action):

    def enable(self, app):
        return app.nr_selected('Patients') != 0

    def run(self, app): 
        for patient in app.selected('Patients'):
            cancel, f = app.dialog.input(
                {"type":"string", "label":"New patient name:", "value": patient.PatientName},
                title = 'Enter new patient name')
            if cancel:
                return
            patient.PatientName = f[0]['value']
        app.refresh()


class SeriesExtractByIndex(wezel.Action):

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):

        # Get source data
        series = app.get_selected(3)[0]
        _, slices = series.get_pixel_array(['SliceLocation', 'AcquisitionTime'])
        series.status.hide()
        nz, nt = slices.shape[0], slices.shape[1]
        x0, x1, t0, t1 = 0, nz, 0, nt

        # Get user input
        invalid = True
        while invalid:
            cancel, f = app.dialog.input(
                {"type":"integer", "label":"Slice location from index..", "value":x0, "minimum": 0, "maximum": nz},
                {"type":"integer", "label":"Slice location to index..", "value":x1, "minimum": 0, "maximum": nz},
                {"type":"integer", "label":"Acquisition time from index..", "value":t0, "minimum": 0, "maximum": nt},
                {"type":"integer", "label":"Acquisition time to index..", "value":t1, "minimum": 0, "maximum": nt},
                title='Select parameter ranges')
            if cancel: 
                return
            x0, x1, t0, t1 = f[0]['value'], f[1]['value'], f[2]['value'], f[3]['value']
            invalid = (x0 >= x1) or (t0 >= t1)
            if invalid:
                app.dialog.information("Invalid selection - first index must be lower than second")

        # Extract series and save
        #study = series.parent().new_sibling(StudyDescription='Extracted Series')
        indices = ' [' + str(x0) + ':' + str(x1) 
        indices += ', ' + str(t0) + ':' + str(t1) + ']'
        #new_series = study.new_child(SeriesDescription = series.SeriesDescription + indices)
        new_series = series.new_sibling(SeriesDescription = slices[0,0,0].SeriesDescription + indices)
        #db.copy_to(slices[x0:x1,t0:t1,:], new_series)
        new_series.adopt(np.ravel(slices[x0:x1,t0:t1,:]).tolist())
        app.refresh()


class SeriesExtractByValue(wezel.Action):

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):

        # Get source data
        series = app.get_selected(3)[0]
        slice_locations = series.SliceLocation
        if not isinstance(slice_locations, list):
            slice_locations = [slice_locations]
        acquisition_times = series.AcquisitionTime
        if not isinstance(acquisition_times, list):
            acquisition_times = [acquisition_times]
        series.status.hide()

        # Get user input
        cancel, f = app.dialog.input(
            {"type":"listview", "label":"Slice locations..", 'list': slice_locations},
            {"type":"listview", "label":"Acquisition times..", 'list': acquisition_times},
            title='Select parameter ranges')
        if cancel: 
            return
        if f[0]['value'] != []:
            slice_locations = [slice_locations[i] for i in f[0]['value']]
        if f[1]['value'] != []:
            acquisition_times = [acquisition_times[i] for i in f[1]['value']]

        # Find matching instances
        all = series.instances()
        instances = []
        for i, instance in enumerate(all):
            series.status.progress(i, len(all), 'Finding instances..')
            v = instance[['SliceLocation', 'AcquisitionTime']]
            if (v[0] in slice_locations) and (v[1] in acquisition_times):
                instances.append(instance)
        series.status.hide()
        if instances == []:
            return

        # Copy matching instances into new series
        series.status.message('Çopying to series..')
        desc = instances[0].SeriesDescription + ' [subseries]'
        new_series = series.new_sibling(SeriesDescription = desc)
        new_series.adopt(instances)
        series.status.hide()
        app.refresh()