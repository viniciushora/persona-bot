(window.webpackJsonp=window.webpackJsonp||[]).push([[42],{1318:function(e,a,t){"use strict";t.r(a);var c=t(0),l=t.n(c),n=t(5),r=t(196),o=t(849);function i(){var e=l.a.useState({checkedA:!0,checkedB:!0}),a=Object(r.a)(e,2),t=a[0],c=a[1],i=function(e){return function(a){c(Object(n.a)(Object(n.a)({},t),{},{[e]:a.target.checked}))}};return l.a.createElement("div",null,l.a.createElement(o.a,{checked:t.checkedA,onChange:i("checkedA"),value:"checkedA",inputProps:{"aria-label":"secondary checkbox"}}),l.a.createElement(o.a,{checked:t.checkedB,onChange:i("checkedB"),value:"checkedB",color:"primary",inputProps:{"aria-label":"primary checkbox"}}),l.a.createElement(o.a,{value:"checkedC",inputProps:{"aria-label":"primary checkbox"}}),l.a.createElement(o.a,{disabled:!0,value:"checkedD",inputProps:{"aria-label":"disabled checkbox"}}),l.a.createElement(o.a,{disabled:!0,checked:!0,value:"checkedE",inputProps:{"aria-label":"primary checkbox"}}),l.a.createElement(o.a,{defaultChecked:!0,value:"checkedF",color:"default",inputProps:{"aria-label":"checkbox with default color"}}))}var d=t(791),m=t(790);function h(){var e=l.a.useState({checkedA:!0,checkedB:!0}),a=Object(r.a)(e,2),t=a[0],c=a[1],i=function(e){return function(a){c(Object(n.a)(Object(n.a)({},t),{},{[e]:a.target.checked}))}};return l.a.createElement(d.a,{row:!0},l.a.createElement(m.a,{control:l.a.createElement(o.a,{checked:t.checkedA,onChange:i("checkedA"),value:"checkedA"}),label:"Secondary"}),l.a.createElement(m.a,{control:l.a.createElement(o.a,{checked:t.checkedB,onChange:i("checkedB"),value:"checkedB",color:"primary"}),label:"Primary"}),l.a.createElement(m.a,{control:l.a.createElement(o.a,{value:"checkedC"}),label:"Uncontrolled"}),l.a.createElement(m.a,{disabled:!0,control:l.a.createElement(o.a,{value:"checkedD"}),label:"Disabled"}),l.a.createElement(m.a,{disabled:!0,control:l.a.createElement(o.a,{checked:!0,value:"checkedE"}),label:"Disabled"}))}var s=t(819),u=t(818),b=t(820);function k(){var e=l.a.useState({gilad:!0,jason:!1,antoine:!0}),a=Object(r.a)(e,2),t=a[0],c=a[1],i=function(e){return function(a){c(Object(n.a)(Object(n.a)({},t),{},{[e]:a.target.checked}))}};return l.a.createElement(u.a,{component:"fieldset"},l.a.createElement(s.a,{component:"legend"},"Assign responsibility"),l.a.createElement(d.a,null,l.a.createElement(m.a,{control:l.a.createElement(o.a,{checked:t.gilad,onChange:i("gilad"),value:"gilad"}),label:"Gilad Gray"}),l.a.createElement(m.a,{control:l.a.createElement(o.a,{checked:t.jason,onChange:i("jason"),value:"jason"}),label:"Jason Killian"}),l.a.createElement(m.a,{control:l.a.createElement(o.a,{checked:t.antoine,onChange:i("antoine"),value:"antoine"}),label:"Antoine Llorca"})),l.a.createElement(b.a,null,"Be careful"))}var p=t(750),E=t(7),g=t(1302),v=t(682),f=t(683),w=Object(E.a)({switchBase:{color:g.a[300],"&$checked":{color:g.a[500]},"&$checked + $track":{backgroundColor:g.a[500]}},checked:{},track:{}})(o.a),y=Object(E.a)(function(e){return{root:{width:42,height:26,padding:0,margin:e.spacing(1)},switchBase:{padding:1,"&$checked":{transform:"translateX(16px)",color:e.palette.common.white,"& + $track":{backgroundColor:"#52d869",opacity:1,border:"none"}},"&$focusVisible $thumb":{color:"#52d869",border:"6px solid #fff"}},thumb:{width:24,height:24},track:{borderRadius:13,border:"1px solid ".concat(e.palette.grey[400]),backgroundColor:e.palette.grey[50],opacity:1,transition:e.transitions.create(["background-color","border"])},checked:{},focusVisible:{}}})(function(e){var a=e.classes,t=Object(p.a)(e,["classes"]);return l.a.createElement(o.a,Object.assign({focusVisibleClassName:a.focusVisible,disableRipple:!0,classes:{root:a.root,switchBase:a.switchBase,thumb:a.thumb,track:a.track,checked:a.checked}},t))}),C=Object(E.a)(function(e){return{root:{width:28,height:16,padding:0,display:"flex"},switchBase:{padding:2,color:e.palette.grey[500],"&$checked":{transform:"translateX(12px)",color:e.palette.common.white,"& + $track":{opacity:1,backgroundColor:e.palette.primary.main,borderColor:e.palette.primary.main}}},thumb:{width:12,height:12,boxShadow:"none"},track:{border:"1px solid ".concat(e.palette.grey[500]),borderRadius:8,opacity:1,backgroundColor:e.palette.common.white},checked:{}}})(o.a);function j(){var e=l.a.useState({checkedA:!0,checkedB:!0,checkedC:!0}),a=Object(r.a)(e,2),t=a[0],c=a[1],o=function(e){return function(a){c(Object(n.a)(Object(n.a)({},t),{},{[e]:a.target.checked}))}};return l.a.createElement(d.a,null,l.a.createElement(m.a,{control:l.a.createElement(w,{checked:t.checkedA,onChange:o("checkedA"),value:"checkedA"}),label:"Custom color"}),l.a.createElement(m.a,{control:l.a.createElement(y,{checked:t.checkedB,onChange:o("checkedB"),value:"checkedB"}),label:"iOS style"}),l.a.createElement(f.a,{component:"div"},l.a.createElement(v.a,{component:"label",container:!0,alignItems:"center",spacing:1},l.a.createElement(v.a,{item:!0},"Off"),l.a.createElement(v.a,{item:!0},l.a.createElement(C,{checked:t.checkedC,onChange:o("checkedC"),value:"checkedC"})),l.a.createElement(v.a,{item:!0},"On"))))}var O=function(){var e=l.a.useState("female"),a=Object(r.a)(e,2),t=a[0],c=a[1];return l.a.createElement(u.a,{component:"fieldset"},l.a.createElement(s.a,{component:"legend"},"labelPlacement"),l.a.createElement(d.a,{"aria-label":"position",name:"position",value:t,onChange:function(e){c(e.target.value)},row:!0},l.a.createElement(m.a,{value:"top",control:l.a.createElement(o.a,{color:"primary"}),label:"Top",labelPlacement:"top"}),l.a.createElement(m.a,{value:"start",control:l.a.createElement(o.a,{color:"primary"}),label:"Start",labelPlacement:"start"}),l.a.createElement(m.a,{value:"bottom",control:l.a.createElement(o.a,{color:"primary"}),label:"Bottom",labelPlacement:"bottom"}),l.a.createElement(m.a,{value:"end",control:l.a.createElement(o.a,{color:"primary"}),label:"End",labelPlacement:"end"})))},B=t(11);a.default=function(){return l.a.createElement("div",{className:"m-sm-30"},l.a.createElement("div",{className:"mb-sm-30"},l.a.createElement(B.a,{routeSegments:[{name:"Material",path:"/material"},{name:"Switch"}]})),l.a.createElement(B.d,{title:"Simple Switch"},l.a.createElement(i,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"Switch with Label"},l.a.createElement(h,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"Switch with Form Group"},l.a.createElement(k,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"Customized Switch"},l.a.createElement(j,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"Switch with Different Label Placement"},l.a.createElement(O,null)))}}}]);
//# sourceMappingURL=42.0671c340.chunk.js.map