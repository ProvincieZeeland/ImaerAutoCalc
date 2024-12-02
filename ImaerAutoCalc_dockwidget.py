import os
import processing
from qgis.utils import iface
from qgis.core import QgsProject, QgsApplication, QgsVectorFileWriter, QgsCoordinateTransformContext, QgsVectorLayer, Qgis, QgsMapLayer, QgsWkbTypes
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QTimer
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox, QPushButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ImaerAutoCalc_dockwidget_base.ui'))

class ImaerAutoCalcDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super(ImaerAutoCalcDockWidget, self).__init__(parent)
        self.setupUi(self)        
        
        # Initialize variables
        self.project = QgsProject.instance()
        self.root = self.project.layerTreeRoot()
        self.groepgever = 'Saldo-gever'
        self.groepnemer = 'Saldo-nemer'
        self.groepoutput = 'Output'
        self.groepexport = 'Export'
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        
        self.imaerpluginname = 'IMAER Plugin'
        self.qgis_plugins_path = QgsApplication.qgisSettingsDirPath() + '/python/plugins'
        self.receptorid_oldversion = 'fid'
        self.receptorid = 'receptor_id'
        self.depositionsum_oldversion = 'dep_TOTAL'
        self.depositionsum = 'deposition_nox_nh3_sum'


        self.startButton.clicked.connect(self.startButtonClicked)
        self.autoButton.clicked.connect(self.autoButtonClicked)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.internSald.clicked.connect(self.internSaldClicked)
        self.mimimum_dep = -0.004444

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def updateContent(self, new_content):
        # Method to update the content of the dock widget
        self.content_widget.setText(new_content)

    def check_group_exist(self, root, group_name):
        # Check if the group's name matches the one you're looking for
        if group_name in [gr.name() for gr in root.children()]:
            # The group exists
            print(f"The group '{group_name}' exists in the project.")
        else:
            # Create the group
            new_group = root.insertGroup(0, group_name)
            print(f"The group '{group_name}' was created in the project.")

    def active_layer(self, layer): 
        return self.root.findLayer(layer).isVisible()

    def layers_in_group(self, gr):
        group = self.root.findGroup(gr)
        if not group:
            return []
        return [layer.layer() for layer in group.findLayers() if self.active_layer(layer.layer())]

    def imaer_diff(self, layers_list):
        custom_outputname = 'Difference'
        # IMAER difference processing tool
        diff_output_layer = processing.run("imaer:relate_difference", 
            {'INPUT_1': layers_list[0],
            'INPUT_2': layers_list[1],
            'ADD_TOTALS':True,
            'OUTPUT':'memory:' + custom_outputname})
        return self.add_to_project(diff_output_layer['OUTPUT'], custom_outputname, self.groepoutput)

    # Function to read version from metadata.txt
    def get_plugin_version(self, plugin_path):
        metadata_file = os.path.join(plugin_path, 'metadata.txt')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as file:
                for line in file:
                    if line.startswith('version='):
                        return line.strip().split('=')[1].strip()
                        
        return 'Version not found'

    def getversionvariables(self):
        # List all directories (each directory represents a plugin)
        plugins = [d for d in os.listdir(self.qgis_plugins_path) if os.path.isdir(os.path.join(self.qgis_plugins_path, d))]

        # Get version of ImaerPlugin
        for plugin in plugins:
            if plugin == 'ImaerPlugin':
                plugin_path = os.path.join(self.qgis_plugins_path, plugin)
                version = self.get_plugin_version(plugin_path)
                version_id = [x for x in version.split(' ')][1]

        # Check if version is 3.5.0 or greater and set the right columnnames for receptor_id and total_deposition
        if version_id >= '3.5.0':
            dep_id = self.receptorid
            dep = self.depositionsum
            return dep_id, dep
        else:
            dep_id = self.receptorid_oldversion
            dep = self.depositionsum_oldversion
            return dep_id, dep

    def check_negatives_of_difference_features(self, diff_output):
        def check_messagebar(widget_destroyed):
                    if not widget_destroyed[0]:
                        message_bar.popWidget(widget)

        def on_widget_destroyed():
                    widget_destroyed[0] = True
        
        dep_id, dep = self.getversionvariables()
        # Iterate through features in the layer and check for negative values
        for feature in diff_output.getFeatures():
            # Ensure the value is numeric and check if it's negative
            if isinstance(feature[dep], (int, float)) and feature[dep] < self.mimimum_dep:
                widget = iface.messageBar().createMessage("Let op!", f"De laag bevat negatieve waarden. Referentie feature: {feature[dep_id]}")
                button = QPushButton(widget)
                button.setText("Zoom naar referentie feature")

                button.pressed.connect(lambda f=feature: self.zoomtofeature(f))
                widget.layout().addWidget(button)
                message_bar = iface.messageBar()
                message_bar.pushWidget(widget, Qgis.Warning)

                widget_destroyed = [False]

                if widget is not None:
                    widget.destroyed.connect(on_widget_destroyed)
                    QTimer.singleShot(5000, lambda: check_messagebar(widget_destroyed))
                break

    def zoomtofeature(self, feature):
        bbox = feature.geometry().boundingBox()

        # Zoom to the combined bounding box
        if not bbox.isEmpty():
            iface.mapCanvas().setExtent(bbox)
            iface.mapCanvas().refresh()

    def filter_polygon_layer(self, layers_list):
        polygon_layers = [
            layer for layer in layers_list
            if layer.type() == QgsMapLayer.VectorLayer
            and QgsWkbTypes.geometryType(layer.wkbType()) == QgsWkbTypes.PolygonGeometry
        ]
        return polygon_layers

    def imaer_sum(self, layers_list, output_name):
        custom_outputname = 'Sum_' + output_name

        layers_list = self.filter_polygon_layer(layers_list)

        # IMAER sum processing tool
        output_layer = processing.run("imaer:relate_sum", 
            {'INPUT_LAYERS': layers_list,
            'ADD_TOTALS':True,
            'OUTPUT':'memory:' + custom_outputname})
        return self.add_to_project(output_layer['OUTPUT'], custom_outputname, self.groepoutput)
    
    def add_to_project(self, output_layer, custom_outputname, group):
        existing_layer = self.project.mapLayersByName(custom_outputname)
        
        if output_layer:
            if existing_layer:
                self.project.removeMapLayer(existing_layer[0].id())
            self.project.addMapLayer(output_layer, False)
            grouppath = self.root.findGroup(group)
            grouppath.addLayer(output_layer)
            return self.project.mapLayersByName(custom_outputname)[0]

    def add_style(self, target_layer, style_file_name):
        qml_style_file = os.path.join(self.script_dir, style_file_name)
        target_layer.loadNamedStyle(qml_style_file)
        target_layer.triggerRepaint()

    def add_multi_style(self, layer, qml_file, style_name):
        if layer and layer.isValid():
            if layer.loadNamedStyle(qml_file):
                print("Style from {} applied successfully".format(qml_file))
                # Associate the style back to the layer using style manager
                style_manager = layer.styleManager()
                style_manager.addStyleFromLayer(style_name)
            else:
                print("Failed to apply style from", qml_file)
        else:
            print("Layer is invalid")

    def layerVisibilityChanged(self, layer):
        allgevers = [layer.layer() for layer in self.root.findGroup(self.groepgever).findLayers()]
        allnemers = [layer.layer() for layer in self.root.findGroup(self.groepnemer).findLayers()]
        layer_list = [x.name() for x in allgevers] + [x.name() for x in allnemers]
        
        if layer.name() in layer_list:
            self.runscript()
            print('Script complete')
        else:
            pass
                
    def runscript(self):
        gevers = self.layers_in_group(self.groepgever)
        nemers = self.layers_in_group(self.groepnemer)
        
        [self.check_group_exist(self.root, x) for x in [self.groepgever, self.groepnemer, self.groepoutput]]

        if gevers: # Sum gevers layers if gevers layers are selected
            totaal_gevers = self.imaer_sum(gevers, self.groepgever)
            layer_node = self.root.findLayer(totaal_gevers)
            if nemers: # Uncheck visability if nemers are selected
                layer_node.setItemVisibilityChecked(False)
            self.add_style(totaal_gevers, os.path.join(self.script_dir,'sum_style.qml'))
        else: # If none selected remove current sum 
            existing_layer = self.project.mapLayersByName('Sum_' + self.groepgever)
            if existing_layer: 
                self.project.removeMapLayer(existing_layer[0].id())

        if nemers: # Sum nemers layers if nemers layers are selected
            totaal_nemers = self.imaer_sum(nemers, self.groepnemer)
            layer_node = self.root.findLayer(totaal_nemers)
            if gevers: # Uncheck visability if gevers are selected
                layer_node.setItemVisibilityChecked(False)
            self.add_style(totaal_nemers, os.path.join(self.script_dir,'sum_style.qml'))
        else: # If none selected remove current sum
            existing_layer = self.project.mapLayersByName('Sum_' + self.groepnemer)
            if existing_layer:
                self.project.removeMapLayer(existing_layer[0].id())

        if bool(gevers and nemers): # Calculate difference if both gevers and nemers are selected
            diff_output = self.imaer_diff([totaal_gevers,totaal_nemers])

            self.check_negatives_of_difference_features(diff_output)          
            layer_node = self.root.findLayer(diff_output)
            
            style_manager = diff_output.styleManager()
            self.add_multi_style(diff_output, os.path.join(self.script_dir, 'diff_style.qml'), 'diff_styling')
            self.add_multi_style(diff_output, os.path.join(self.script_dir, 'diff_two_color.qml'), 'default')
            self.project.addMapLayer(diff_output)
            layer_node.setExpanded(False)


        else: # Remove current difference layer if gevers- and nemers layer are both not selected
            existing_layer = self.project.mapLayersByName('Difference')
            if existing_layer:
                self.project.removeMapLayer(existing_layer[0].id())

    def startButtonClicked(self):
        print("Start button clicked!")
        self.runscript()

    def autoButtonClicked(self):
        print("AutoCalc button clicked!")
        # Toggle the script on or off based on the current state
        if not hasattr(self, 'scriptIsActive'):
            self.scriptIsActive = False  # Initialize the flag if it doesn't exist
        self.scriptIsActive = not self.scriptIsActive  # Toggle the flag
        if self.scriptIsActive:
            self.autoButton.setStyleSheet("background-color: #55C74D;")
            self.connection = self.project.layerTreeRoot().visibilityChanged.connect(self.layerVisibilityChanged)
            print("The plugin is turned on.")
        else:
            # Script is deactivated, disconnect the signal
            self.project.layerTreeRoot().visibilityChanged.disconnect(self.connection)
            self.autoButton.setStyleSheet("background-color: #F0F0F0;")

    def select_driver(self, output_file_path):
        # Determine the driver based on the selected file format
            if output_file_path.endswith('.gpkg'):
                driver_name = 'GPKG'
            elif output_file_path.endswith('.csv'):
                driver_name = 'CSV'
            elif output_file_path.endswith('.xlsx'):
                driver_name = 'XLSX'
            else:
                # Default to GeoPackage if the file format is not recognized
                driver_name = 'GPKG'
                output_file_path += '.gpkg'  # Default to GeoPackage extension
            return driver_name, output_file_path

    def saveButtonClicked(self):
        print("Save button clicked!")
        # Add group 'Export' to the project
        self.check_group_exist(self.root, self.groepexport)

        # Get the 'Difference' layer
        difference_layer = self.project.mapLayersByName('Difference')[0]
        self.export_file(difference_layer)
        
    def export_file(self, layer):
        # Open a file dialog for saving the GeoPackage file
        output_file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "GeoPackage files (*.gpkg);;CSV files (*.csv);;Excel files (*.xlsx)")
        
        # Check if the user canceled the dialog
        if output_file_path:

            driver_name, output_file_path = self.select_driver(output_file_path)
            
            # Export features to GeoPackage
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = driver_name
            options.fileEncoding = "UTF-8"
            
            error = QgsVectorFileWriter.writeAsVectorFormatV3(layer,
                                                            output_file_path,
                                                            QgsCoordinateTransformContext(),
                                                            options)
            
            if error[0] == QgsVectorFileWriter.NoError:
                print("Export successful!")
            
                layer_name = os.path.splitext(os.path.basename(output_file_path))[0]

                if driver_name in ('CSV', 'XLSX'):
                    iface.messageBar().pushMessage(f"{layer_name}", f" is opgeslagen.", level=Qgis.Info)
                
                if driver_name == 'GPKG':
                    # Add the exported file to the project
                    uri = f"{output_file_path}|layername={layer_name}"
                    saved_layer = QgsVectorLayer(uri, layer_name, "ogr")
                    
                    self.add_to_project(saved_layer, layer_name, self.groepexport)
                    print(f'Added the layer {layer_name}')

                    # Add multiple styles
                    style_manager = saved_layer.styleManager()
                    self.add_multi_style(saved_layer, os.path.join(self.script_dir, 'diff_style.qml'), 'diff_styling')
                    self.add_multi_style(saved_layer, os.path.join(self.script_dir, 'diff_two_color.qml'), 'default')

                    layer_node = self.root.findLayer(saved_layer)
                    layer_node.setExpanded(False)
            else:
                error_message = f"Export failed with error code {error[0]}: {error[1]}"
                print(error_message)
                iface.messageBar().pushMessage("Error", f"De laag is niet geëxporteerd, verwijder lagen met dezelfde naam: {error_message}", level=Qgis.Critical)
                
        else:
            print("Export canceled by the user.")

    def internSaldClicked(self):
        dep_id, dep = self.getversionvariables()
        diff_output = self.project.mapLayersByName('Difference')[0]
        self.check_group_exist(self.root, self.groepexport)
        internsald = QgsVectorLayer(diff_output.source(), 'internsald', 'memory')
        internsald_data_provider = internsald.dataProvider()
        dep_total_idx = internsald.fields().indexFromName(dep)
        
        # Filter values greater than 0
        selected_features = []
        for feature in diff_output.getFeatures():
            if feature.attributes()[dep_total_idx] > 0:
                selected_features.append(feature)
        
        # Export selected features
        internsald_data_provider.addFeatures(selected_features)
        internsald.updateExtents()
        self.export_file(internsald)
        print(f'Added the layer internsald')