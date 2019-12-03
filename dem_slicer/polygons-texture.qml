<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology" version="3.10.0-A Coruña">
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol name="0" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="RasterFill" pass="0" locked="0">
          <prop k="alpha" v="0.749"/>
          <prop k="angle" v="0"/>
          <prop k="coordinate_mode" v="0"/>
          <prop k="imageFile" v="W:/GitHub/dem_slicer/tex-scan.png"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="width" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="width_unit" v="Pixel"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="alpha" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="scale_linear( &quot;num&quot; , minimum(&quot;num&quot;), maximum(&quot;num&quot;), 0, 100)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="angle" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="randf(0, 360)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerGeometryType>2</layerGeometryType>
</qgis>
