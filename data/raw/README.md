# Data

Data from [here](https://maps.nrel.gov/re-atlas/?aL=0&bL=clight&cE=0&lR=0&mC=37.56199695314352%2C-94.306640625&zL=5)

***YOU HAVE TO DOWNLOAD us_csp_total.kml IT IS THE CONCENTRATED SOLAR POWER - NOT THE FILTERED ONE. PUT IT WITH THE REST OF THE KML FILES!!!***


|      File name      |                 Description                 |
| :-----------------: | :-----------------------------------------: |
|     biomass.kml     |                biomass data                 |
|   wave_energy.csv   |             wave power density              |
|  us_csp_total.kml   | Concentrated Solar Power Total (unfiltered) |
|  us_geothermal.kml  |               Geothermal data               |
|   smallhydro.kml    |      Feasible Small hydro project data      |
| NonPowered_Dams.kml |            Nonpowered dams data             |

## Note about data.

CSV files do not provide us with coordinates except for one. Their ID do not seem to have a correlation that can be predicted and mapped.

KML files have coordinates. They are located within a LookAt tag

```xml
<LookAt>
    <longitude>-86.23419538650211</longitude>
    <latitude>37.99907740964661</latitude>
    <altitude>78364.97296392133</altitude>
    <heading>0.0</heading>
    <tilt>0.0</tilt>
    <range>63323.00852857447</range>
    <altitudeMode>clampToGround</altitudeMode>
</LookAt>
```

KML files need to be parsed by an XML parser which is more annoying. They also contain a huge chunk of text which is html written with escape sequences. These sections are found under the description tag.

```
&lt;ul class="textattributes"&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;gid&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;2068&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;name&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;Meade&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;state_name&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;Kentucky&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;state_fips&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;21&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;cnty_fips&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;163&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;fips&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;21163&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;area&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;324.20779&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;pop2000&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;26349&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;crops&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;12483.597&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;manure&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;355.678&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;forest&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;15432.000&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;primmill&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;0.000&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;secmill&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;244.800&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;urban&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;3037.085&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;landfill&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;0.000&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;wwtf&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;43.571&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;swg&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;29094.811&lt;/span&gt;&lt;/li&gt;
  &lt;li&gt;&lt;strong&gt;&lt;span class="atr-name"&gt;total&lt;/span&gt;:&lt;/strong&gt; &lt;span class="atr-value"&gt;60691.542&lt;/span&gt;&lt;/li&gt;
 ``` 

This section contains the data but it is wrapped with html.