(window.webpackJsonp=window.webpackJsonp||[]).push([[38],{1321:function(e,a,t){"use strict";t.r(a);var n=t(0),l=t.n(n),r=t(196),o=t(680),c=t(659),i=t(821);var u=function(){var e=l.a.useState(null),a=Object(r.a)(e,2),t=a[0],n=a[1];function u(){n(null)}return l.a.createElement("div",null,l.a.createElement(o.a,{variant:"outlined","aria-owns":t?"simple-menu":void 0,"aria-haspopup":"true",onClick:function(e){n(e.currentTarget)}},"Open Menu"),l.a.createElement(c.a,{id:"simple-menu",anchorEl:t,open:Boolean(t),onClose:u},l.a.createElement(i.a,{onClick:u},"Profile"),l.a.createElement(i.a,{onClick:u},"My account"),l.a.createElement(i.a,{onClick:u},"Logout")))},m=t(654),s=t(675),p=t(817),d=t(1109),E=Object(m.a)(function(e){return{root:{width:"100%",maxWidth:360,backgroundColor:e.palette.background.paper}}}),v=["Show some love to Material-UI","Show all notification content","Hide sensitive notification content","Hide all notification content"];function f(){var e=E(),a=l.a.useState(null),t=Object(r.a)(a,2),n=t[0],o=t[1],u=l.a.useState(1),m=Object(r.a)(u,2),f=m[0],b=m[1];return l.a.createElement("div",{className:e.root},l.a.createElement(s.a,{component:"nav","aria-label":"Device settings"},l.a.createElement(p.a,{button:!0,"aria-haspopup":"true","aria-controls":"lock-menu","aria-label":"When device is locked",onClick:function(e){o(e.currentTarget)}},l.a.createElement(d.a,{primary:"When device is locked",secondary:v[f]}))),l.a.createElement(c.a,{id:"lock-menu",anchorEl:n,keepMounted:!0,open:Boolean(n),onClose:function(){o(null)}},v.map(function(e,a){return l.a.createElement(i.a,{key:e,disabled:0===a,selected:a===f,onClick:function(e){return function(e,a){b(a),o(null)}(0,a)}},e)})))}var b=t(7),h=t(1303),k=t(1155),g=t.n(k),y=t(1154),C=t.n(y),w=t(1153),O=t.n(w),M=Object(b.a)({paper:{border:"1px solid #d3d4d5"}})(function(e){return l.a.createElement(c.a,Object.assign({elevation:0,getContentAnchorEl:null,anchorOrigin:{vertical:"bottom",horizontal:"center"},transformOrigin:{vertical:"top",horizontal:"center"}},e))}),S=Object(b.a)(function(e){return{root:{"&:focus":{backgroundColor:e.palette.primary.main,"& .MuiListItemIcon-root, & .MuiListItemText-primary":{color:e.palette.common.white}}}}})(i.a);var j=function(){var e=l.a.useState(null),a=Object(r.a)(e,2),t=a[0],n=a[1];return l.a.createElement("div",null,l.a.createElement(o.a,{"aria-owns":t?"simple-menu":void 0,"aria-haspopup":"true",variant:"contained",color:"primary",onClick:function(e){n(e.currentTarget)}},"Open Menu"),l.a.createElement(M,{id:"simple-menu",anchorEl:t,open:Boolean(t),onClose:function(){n(null)}},l.a.createElement(S,null,l.a.createElement(h.a,null,l.a.createElement(O.a,null)),l.a.createElement(d.a,{primary:"Sent mail"})),l.a.createElement(S,null,l.a.createElement(h.a,null,l.a.createElement(C.a,null)),l.a.createElement(d.a,{primary:"Drafts"})),l.a.createElement(S,null,l.a.createElement(h.a,null,l.a.createElement(g.a,null)),l.a.createElement(d.a,{primary:"Inbox"}))))},x=t(677),N=t(670),T=["None","Atria","Callisto","Dione","Ganymede","Hangouts Call","Luna","Oberon","Phobos","Pyxis","Sedna","Titania","Triton","Umbriel"],P=48;var I=function(){var e=l.a.useState(null),a=Object(r.a)(e,2),t=a[0],n=a[1],o=Boolean(t);function u(){n(null)}return l.a.createElement("div",null,l.a.createElement(x.a,{"aria-label":"More","aria-owns":o?"long-menu":void 0,"aria-haspopup":"true",onClick:function(e){n(e.currentTarget)}},l.a.createElement(N.a,null,"more_vert")),l.a.createElement(c.a,{id:"long-menu",anchorEl:t,open:o,onClose:u,PaperProps:{style:{maxHeight:4.5*P,width:200}}},T.map(function(e){return l.a.createElement(i.a,{key:e,selected:"Pyxis"===e,onClick:u},e)})))},B=t(11);a.default=function(){return l.a.createElement("div",{className:"m-sm-30"},l.a.createElement("div",{className:"mb-sm-30"},l.a.createElement(B.a,{routeSegments:[{name:"Material",path:"/material"},{name:"Menu"}]})),l.a.createElement(B.d,{title:"simple menu"},l.a.createElement(u,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"selected menu"},l.a.createElement(f,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"customized menu"},l.a.createElement(j,null)),l.a.createElement("div",{className:"py-12"}),l.a.createElement(B.d,{title:"max height menu"},l.a.createElement(I,null)))}}}]);
//# sourceMappingURL=38.237ea975.chunk.js.map