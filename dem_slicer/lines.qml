<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology" version="3.10.0-A Coruña">
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol name="0" alpha="0.7" type="line" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" class="SimpleLine" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="169,142,142,176"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.02"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="set_color_part( @symbol_color , 'alpha',  scale_linear( &quot;num&quot; , minimum(&quot;num&quot;), maximum(&quot;num&quot;), 100, 255) )"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="scale_exp( &quot;num&quot; , minimum(&quot;num&quot;), maximum(&quot;num&quot;), 0.02, 0.3, 0.6)"/>
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
  <featureBlendMode>6</featureBlendMode>
  <layerGeometryType>1</layerGeometryType>
</qgis>
