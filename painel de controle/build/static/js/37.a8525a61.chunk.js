(window.webpackJsonp=window.webpackJsonp||[]).push([[37],{1333:function(e,t,a){"use strict";a.r(t);var n=a(33),r=a(34),l=a(36),o=a(35),i=a(0),c=a.n(i),s=a(9),m=a(684),p=a(795),h=a(860),u=Object(p.compose)(Object(p.withProps)({googleMapURL:"https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places",loadingElement:c.a.createElement("div",{style:{height:"100%"}}),containerElement:c.a.createElement("div",{style:{height:"400px"}}),mapElement:c.a.createElement("div",{style:{height:"100%"}})}),h.withScriptjs,h.withGoogleMap)(function(e){return c.a.createElement(h.GoogleMap,{defaultZoom:8,defaultCenter:{lat:-34.397,lng:150.644}})}),d=a(1275),g=Object(p.compose)(Object(p.withProps)({googleMapURL:"https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places",loadingElement:c.a.createElement("div",{style:{height:"100%"}}),containerElement:c.a.createElement("div",{style:{height:"400px"}}),mapElement:c.a.createElement("div",{style:{height:"100%"}})}),h.withScriptjs,h.withGoogleMap)(function(e){return c.a.createElement(h.GoogleMap,{defaultZoom:8,defaultCenter:{lat:-34.397,lng:150.644}},c.a.createElement(h.Marker,{isMarkerShown:!1,position:{lat:-34.397,lng:150.644},onClick:e.onMarkerClick},c.a.createElement(d.InfoBox,{options:{closeBoxURL:"",enableEventPropagation:!0}},c.a.createElement(m.a,{className:"p-16"},c.a.createElement("p",{className:"white-space-pre m-0"},"Hello World !!!")))))}),E=function(e){Object(l.a)(a,e);var t=Object(o.a)(a);function a(){var e;Object(n.a)(this,a);for(var r=arguments.length,l=new Array(r),o=0;o<r;o++)l[o]=arguments[o];return(e=t.call.apply(t,[this].concat(l))).state={isMarkerShown:!1},e.delayedShowMarker=function(){e.timer=setTimeout(function(){e.setState({isMarkerShown:!0})},3e3)},e.handleMarkerClick=function(){e.setState({isMarkerShown:!1}),e.delayedShowMarker()},e}return Object(r.a)(a,[{key:"componentDidMount",value:function(){this.delayedShowMarker()}},{key:"componentWillUnmount",value:function(){this.timer&&clearTimeout(this.timer)}},{key:"render",value:function(){return c.a.createElement(g,{isMarkerShown:this.state.isMarkerShown,onMarkerClick:this.handleMarkerClick})}}]),a}(c.a.PureComponent),w=function(e){Object(l.a)(a,e);var t=Object(o.a)(a);function a(){var e;Object(n.a)(this,a);for(var r=arguments.length,l=new Array(r),o=0;o<r;o++)l[o]=arguments[o];return(e=t.call.apply(t,[this].concat(l))).state={},e}return Object(r.a)(a,[{key:"render",value:function(){return c.a.createElement("div",{className:"m-sm-30"},c.a.createElement("div",{className:"mb-sm-30"},c.a.createElement(s.a,{routeSegments:[{name:"Map"}]})),c.a.createElement(m.a,null,c.a.createElement(u,null)),c.a.createElement("div",{className:"py-12"}),c.a.createElement(m.a,null,c.a.createElement(E,null)))}}]),a}(i.Component);t.default=w}}]);
//# sourceMappingURL=37.a8525a61.chunk.js.map