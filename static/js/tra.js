$(function(){

	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('map').setView([51.505, -0.09], 11);
	var control = L.control.layers();
	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	var control = L.control.layers().addTo(map);

	

	var Testlist = function(period){
		this.el=$('#sidebar');
		this.period=period;
		var url = '/test/'+period+'/';
		var datalist = new Array();
		this.render = function(){
			var period = this.period;
			var title = "<h3 class='navbar-title'>Experiments   "+period+"s</h3>";
			this.el.html(title);
			var listel = $('<ul class="nav nav-sidebar"></ul>');
			datalist.forEach(function(row){
				listel.append($('<li><a href="#test/'+period+'/'+row.id+'"><span class="span-id">TEST '+row.testid+'</span><span class="span-num">'+row.num+' Routes'+'</span></a></li>'));
			});
			this.el.append(listel);
			this.el.on('click','li',function(){
				var that=$(this);
				if(!that.hasClass('active')){
					$('#sidebar .active').removeClass('active');
					that.addClass('active');
				}
			});
		};
		this.fetch = function(){
			var that=this;
			$.ajax(url,{
				success:function(data){
					for(var i=0, len=data.length; i<len; i++){
						datalist[i]={id:data[i]['id'],num:data[i]['num'],testid:data[i]['testid']};
					}
				},
				complete:function(){
					that.render();
				}
			});
		};
	};


	var Testview =Backbone.View.extend({
		tagName: 'tbody',
		className: 'route-table',
		map: map,
		layergroup: L.featureGroup(),
		layerControl: control, 
		activateRoute:undefined,
		events:{
			"click .route" : "activate"
		},
		activate:function(e){
			var thatcolor=this.getColor;
			var selectedrow=$(e.target).closest('.route');
			var colorPos = selectedrow.children().eq(1);
			selectedrow.siblings('.active').removeClass('active');
			selectedrow.addClass('.active');

			if(this.activateRoute){
				this.activateRoute.setStyle(function(){
					return {
						color:thatcolor(parseFloat(colorPos)),
						weight:3,
						opacity: 0.5,
						lineCap: 'round'
					};
				});
			}
			selectedrow.data('geom').setStyle(function(){
				return {
					color: 'blue',
					weight:7,
					opacity:0.8
				};
			});
			this.activateRoute=selectedrow.data('geom');
		},
		initialize:function(){
			this.listenTo(this.model, "change",this.render); 
		},
		render:function(){
			// var tablerows = this.template(this.model.attributes);
			var routes = this.model.get('routes');
			for(var i = 0, len=routes.length; i< len; i++){
				this.$el.append(this.singlerow(i,routes[i]));
			}
			// var tablerows = this.mytemplate(this.model.get('routes'));
			// this.$el.html(tablerows);
			$('.route-table-header').after(this.$el);
			sort.refresh();
			this.maprender();
			this.rendercharts();
		},
		mytemplate:function(routes){
			var routesnum = routes.length;
			var htmltext="";
			for(var i=0; i<routesnum; i++){
				htmltext+="<tr class='route' data-id='"+i+"'>";
				htmltext+="<td>"+(i+1)+"</td>";
				htmltext+="<td>"+routes[i].possibility.toFixed(3)+"</td>";
				htmltext+="<td>"+routes[i].RMSE.toFixed(3)+"</td>";
				htmltext+="<td>"+routes[i].TRMSE.toFixed(3)+"</td>";
				htmltext+="<td>"+routes[i].area.toFixed(3)+"</td>";
				htmltext+="<td>"+routes[i].CLength.toFixed(3)+"</td>";
				htmltext+="</tr>";
			}
			return htmltext;
		},
		getColor:function(d){
			return d > 0.7 ? '#800026' :
		           d > 0.6  ? '#BD0026' :
		           d > 0.5  ? '#E31A1C' :
		           d > 0.4  ? '#FC4E2A' :
		           d > 0.3   ? '#FD8D3C' :
		           d > 0.2  ? '#FEB24C' :
		           d > 0.1   ? '#FED976' :
		                      '#FFEDA0';
		},
		maprender:function(){
			var thatcolor=this.getColor;
			var thatlayergroup = this.layergroup;
			var truePath = this.model.get('test_para');
			var measurementslayer = L.geoJson(truePath.measurements);
			var truepathlayer=L.geoJson(truePath.truepath,{
				style:function(){
					return {
						weight:2,
						color: 'red',
						dashArray: '3',
						lineCap: 'round'
					};
				}
			});
			var projectedlayer=L.geoJson(truePath.projected,{
				pointToLayer: function(feature, latlng){
					return L.circleMarker(latlng,{
						weight:7,
						color:'#CC6600',
						opacity: 1.0
					});
				}
			});
			thatlayergroup.addLayer(measurementslayer);
			thatlayergroup.addLayer(truepathlayer);
			thatlayergroup.addLayer(projectedlayer);
			this.layerControl.addOverlay(measurementslayer,"Measurements");
			this.layerControl.addOverlay(truepathlayer,"True Path");
			this.layerControl.addOverlay(projectedlayer,"Fixes on Path");
			thatlayergroup.addTo(this.map);
			this.map.fitBounds(measurementslayer.getBounds());
		},
		singlerow:function(i,route){
			var thatcolor=this.getColor;
			var htmltext='';
			htmltext+="<tr class='route' data-id='"+i+"'>";
			htmltext+="<td data-sort='"+(i+1)+"'>"+(i+1)+"</td>";
			htmltext+="<td>"+route.possibility.toFixed(3)+"</td>";
			htmltext+="<td>"+route.RMSE.toFixed(3)+"</td>";
			htmltext+="<td>"+route.TRMSE.toFixed(3)+"</td>";
			htmltext+="<td>"+route.area.toFixed(3)+"</td>";
			htmltext+="<td>"+route.CLength.toFixed(3)+"</td>";
			htmltext+="</tr>";
			var htmlel = $(htmltext);
			var layer = L.geoJson(route.modeledpath,{
					style:function(){
						return {
							weight:3,
							color:thatcolor(route.possibility),
							opacity: 0.5,
							lineCap: 'round'
						};
					}
				});
			this.layergroup.addLayer(layer);
			htmlel.data('geom',layer);
			return htmlel
		},
		destorylayer:function(){
			var thatcontrol = this.layerControl
			this.layergroup.eachLayer(function(layer){
				thatcontrol.removeLayer(layer);
			});
			this.layergroup.clearLayers();
			this.map.removeLayer(this.layergroup);
		},
		renderchart:function(index){
			var routes = this.model.get('routes');
			var data = [];
			for (var i = 0; i < routes.length; i++) {
				data.push([routes[i].possibility,routes[i][index]]);
			}
			$('#chart-'+index).highcharts({
				chart:{
					type:'scatter',
					zoomType:'xy'
				},
				title:{
					text: 'possibility vs. '+index
				},
				xAxis:{
					title:{
						enabled:true,
						text:'probability'
					},
					startOnTick:true,
					endOnTick:true,
					showLastLabel:true
				},
				yAxis:{
					title:{
						text:index + ' value'
					}
				},
				plotOptions:{
					scatter:{
						marker: {
							radius:4,
							states:{
								hover:{
									enabled:true,
									lineColor: 'rgb(100,100,100)'
								}
							}
						},
						states:{
							hover:{
								marker:{
									enabled: false
								}
							}
						},
						tooltip:{
							pointFormat: '{point.x}, {point.y}'
						}
					}
				},
				series:[{
					color:'rgba(223,83,83,.5)',
					data:data
				}]
			});
		},
		rendercharts:function(){
			this.renderchart('RMSE');
			this.renderchart('TRMSE');
			this.renderchart('area');
			this.renderchart('CLength');
		}
	});

	var TraRouter = Backbone.Router.extend({
		default:{
			activemodel:undefined,
			activeview:undefined
		},
		routes:{
			"test/:t/:id": "singletest",
			"list/:time": "period",
		},
		period:function(time){
			var testlistobj = new Testlist(time);
			testlistobj.fetch();
		},
		singletest:function(t,id){
			var Test = Backbone.Model.extend({urlRoot:'/test/'+t});
			if(this.activeview){
				this.activeview.destorylayer();
				this.activeview.remove();
			}
			this.activemodel = new Test({id:id});
			this.activeview =new Testview({model:this.activemodel});
			this.activemodel.fetch();
		}
	});


	var approuter=new TraRouter;
	Backbone.history.start();
	var table = document.getElementById('sta-table');
	var sort = new Tablesort(table);
	var tabs = $("#tabs").tabs();
	
});