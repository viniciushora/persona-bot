(window.webpackJsonp=window.webpackJsonp||[]).push([[30],{1315:function(e,t,a){"use strict";a.r(t);var n=a(5),i=a(33),o=a(34),c=a(36),r=a(35),l=a(0),s=a.n(l),d=a(94),u=a(3),m=a.n(u),p=a(77),b=a(7),f=a(893),g=a.n(f),h=a(68),v=a(275),y=a(17),S=a(653),O=a(677),j=a(670),E=a(196),N=a(1311),x=a(1312),k=a(684),w=a(680),_=a(57),C=a(636),T=a(116);var L=Object(C.a)({},{withTheme:!0})(Object(d.b)(function(e){return{createNotification:u.PropTypes.func.isRequired,getNotification:u.PropTypes.func.isRequired,deleteNotification:u.PropTypes.func.isRequired,deleteAllNotification:u.PropTypes.func.isRequired,notification:e.notification,settings:e.layout.settings}},{createNotification:T.e,getNotification:T.h,deleteNotification:T.g,deleteAllNotification:T.f})(function(e){var t=e.container,a=e.theme,n=e.settings,i=e.notification,o=void 0===i?[]:i,c=e.getNotification,r=e.deleteAllNotification,l=e.deleteNotification,d=s.a.useState(!1),u=Object(E.a)(d,2),m=u[0],p=u[1],b=setInterval(function(){c(),clearInterval(b)},5e3);function f(){m||c(),p(!m)}var g=a.palette;return s.a.createElement(S.a,{theme:n.themes[n.activeTheme]},s.a.createElement(O.a,{onClick:f,style:{color:"light"===g.type?g.text.secondary:g.text.primary}},s.a.createElement(N.a,{color:"secondary",badgeContent:o.length},s.a.createElement(j.a,null,"notifications"))),s.a.createElement(x.a,{width:"100px",container:t,variant:"temporary",anchor:"right",open:m,onClose:f,ModalProps:{keepMounted:!0}},s.a.createElement("div",{className:"notification"},s.a.createElement("div",{className:"notification__topbar flex flex-middle p-16 mb-24"},s.a.createElement(j.a,{color:"primary"},"notifications"),s.a.createElement("h5",{className:"ml-8 my-0 font-weight-500"},"Notifica\xe7\xf5es")),o.map(function(e){return s.a.createElement("div",{key:e.id,className:"notification__card position-relative"},s.a.createElement(O.a,{size:"small",className:"delete-button bg-light-gray mr-24",onClick:function(){return l(e.id)}},s.a.createElement(j.a,{className:"text-muted",fontSize:"small"},"clear")),s.a.createElement(_.a,{to:"/".concat(e.path),onClick:f},s.a.createElement(k.a,{className:"mx-16 mb-24",elevation:3},s.a.createElement("div",{className:"card__topbar flex flex-middle flex-space-between p-8 bg-light-gray"},s.a.createElement("div",{className:"flex"},s.a.createElement("div",{className:"card__topbar__button"},s.a.createElement(j.a,{className:"card__topbar__icon",fontSize:"small",color:e.icon.color},e.icon.name)),s.a.createElement("span",{className:"ml-4 font-weight-500 text-muted"},e.heading)),s.a.createElement("small",{className:"card__topbar__time text-muted"},Object(h.c)(new Date(e.timestamp))," ago")),s.a.createElement("div",{className:"px-16 pt-8 pb-16"},s.a.createElement("p",{className:"m-0"},e.title),s.a.createElement("small",{className:"text-muted"},e.subtitle)))))}),s.a.createElement("div",{className:"text-center"},s.a.createElement(w.a,{onClick:r},"Limpar notifica\xe7\xf5es")))))})),P=function(e){Object(c.a)(a,e);var t=Object(r.a)(a);function a(){var e;Object(i.a)(this,a);for(var o=arguments.length,c=new Array(o),r=0;r<o;r++)c[r]=arguments[r];return(e=t.call.apply(t,[this].concat(c))).state={},e.updateSidebarMode=function(t){var a=e.props,i=a.settings;(0,a.setLayoutSettings)(Object(n.a)(Object(n.a)({},i),{},{layout1Settings:Object(n.a)(Object(n.a)({},i.layout1Settings),{},{leftSidebar:Object(n.a)(Object(n.a)({},i.layout1Settings.leftSidebar),t)})}))},e.handleSidebarToggle=function(){var t,a=e.props.settings.layout1Settings;t=Object(h.d)()?"close"===a.leftSidebar.mode?"mobile":"close":"full"===a.leftSidebar.mode?"close":"full",e.updateSidebarMode({mode:t})},e.handleSignOut=function(){e.props.logoutUser()},e}return Object(o.a)(a,[{key:"render",value:function(){var e=this.props,t=e.theme,a=e.settings,n=e.className,i=e.style,o=a.themes[a.layout1Settings.topbar.theme]||t;return s.a.createElement(S.a,{theme:o},s.a.createElement("div",{className:"topbar"},s.a.createElement("div",{className:"topbar-hold ".concat(n),style:Object.assign({},{backgroundColor:o.palette.primary.main},i)},s.a.createElement("div",{className:"flex flex-space-between flex-middle h-100"},s.a.createElement("div",{className:"flex"},s.a.createElement(O.a,{onClick:this.handleSidebarToggle},s.a.createElement(j.a,null,"menu"))),s.a.createElement("div",{className:"flex flex-middle"},s.a.createElement(L,null))))))}}]),a}(l.Component),R=Object(b.a)(function(e){return{root:{backgroundColor:e.palette.primary.main}}},{withTheme:!0})(Object(y.g)(Object(d.b)(function(e){return{setLayoutSettings:u.PropTypes.func.isRequired,logoutUser:u.PropTypes.func.isRequired,settings:e.layout.settings}},{setLayoutSettings:p.d})(P))),M=a(849),q=[{name:"In\xedcio",path:"/dashboard/inicio",icon:"dashboard"},{name:"Cadastro",icon:"description",children:[{name:"Personagem",path:"/cadastro/personagem",iconText:"P1"},{name:"Persona",path:"/cadastro/persona",iconText:"P2"},{name:"Shadow",path:"/cadastro/shadow",iconText:"S"},{name:"Item",path:"/cadastro/item",iconText:"I"},{name:"Habilidade",path:"/cadastro/habilidade",iconText:"H"}]},{name:"Listagem (WIP)",icon:"format_list_bulleted",path:"/naoexiste"},{name:"Edi\xe7\xe3o (WIP)",icon:"edit",path:"/naoexiste"},{name:"Configura\xe7\xf5es",path:"/config",icon:"settings"}],A=a(11),I=function(e){Object(c.a)(a,e);var t=Object(r.a)(a);function a(){var e;Object(i.a)(this,a);for(var o=arguments.length,c=new Array(o),r=0;r<o;r++)c[r]=arguments[r];return(e=t.call.apply(t,[this].concat(c))).state={},e.updateSidebarMode=function(t){var a=e.props,i=a.settings,o=a.setLayoutSettings,c=i.activeLayout+"Settings",r=i[c];o(Object(n.a)(Object(n.a)({},i),{},{[c]:Object(n.a)(Object(n.a)({},r),{},{leftSidebar:Object(n.a)(Object(n.a)({},r.leftSidebar),t)})}))},e.renderOverlay=function(){return s.a.createElement("div",{onClick:function(){return e.updateSidebarMode({mode:"close"})},className:"sidenav__overlay"})},e}return Object(o.a)(a,[{key:"render",value:function(){return s.a.createElement(l.Fragment,null,s.a.createElement(g.a,{option:{suppressScrollX:!0},className:"scrollable position-relative"},this.props.children,s.a.createElement(A.c,{navigation:q})),this.renderOverlay())}}]),a}(l.Component),U=Object(y.g)(Object(d.b)(function(e){return{setLayoutSettings:m.a.func.isRequired,settings:e.layout.settings}},{setLayoutSettings:p.d})(I)),W=function(e){Object(c.a)(a,e);var t=Object(r.a)(a);function a(){var e;Object(i.a)(this,a);for(var n=arguments.length,o=new Array(n),c=0;c<n;c++)o[c]=arguments[c];return(e=t.call.apply(t,[this].concat(o))).state={},e}return Object(o.a)(a,[{key:"render",value:function(){return s.a.createElement("div",{className:"flex flex-middle flex-space-between brand-area"},s.a.createElement("div",{className:"flex flex-middle brand"},s.a.createElement("span",{className:"brand__text"},"PersonaBot")),this.props.children)}}]),a}(l.Component),z=a(252),D=function(e){var t=e.theme,a=e.settings;return s.a.createElement(z.Helmet,null,s.a.createElement("style",null,"\n        \n        ".concat("dark"===t.palette.type?".sidenav {\n          color: ".concat(t.palette.text.secondary,";\n        }"):" ","\n\n        .sidenav__hold {\n          background-image: url(").concat(a.layout1Settings.leftSidebar.bgImgURL,");\n          opacity: 1 !important;\n        }\n        .sidenav__hold::after {\n          background: ").concat(t.palette.primary.main,";\n          opacity: ").concat(a.layout1Settings.leftSidebar.bgOpacity,";\n        }\n        .navigation .nav-item:not(.badge) {\n          color: ").concat(t.palette.text.primary,";\n        }\n        .navigation .nav-item .icon-text::after {\n          background: ").concat(t.palette.text.primary,";\n        }\n        .navigation .nav-item.active, \n        .navigation .nav-item.active:hover {\n          background: ").concat(t.palette.secondary.main,";\n        }\n\n        \n        ").concat("dark"===t.palette.type?".navigation .nav-item:hover,\n        .navigation .nav-item.active {\n          color: ".concat(t.palette.text.primary,";\n        }"):"","\n        \n      ")))},H=(Object(b.a)(function(e){return{root:{backgroundColor:"transparent",padding:"5px"}}})(O.a),Object(b.a)(function(){return{root:{fontSize:"1rem"}}})(j.a),function(e){Object(c.a)(a,e);var t=Object(r.a)(a);function a(){var e;Object(i.a)(this,a);for(var o=arguments.length,c=new Array(o),r=0;r<o;r++)c[r]=arguments[r];return(e=t.call.apply(t,[this].concat(c))).state={sidenavToggleChecked:!1},e.updateSidebarMode=function(t){var a=e.props,i=a.settings,o=a.setLayoutSettings,c=a.setDefaultSettings,r=Object(n.a)(Object(n.a)({},i),{},{layout1Settings:Object(n.a)(Object(n.a)({},i.layout1Settings),{},{leftSidebar:Object(n.a)(Object(n.a)({},i.layout1Settings.leftSidebar),t)})});o(r),c(r)},e.handleSidenavToggle=function(){var t=e.state.sidenavToggleChecked,a=t?"full":"compact";e.updateSidebarMode({mode:a}),e.setState({sidenavToggleChecked:!t})},e.handleSignOut=function(){e.props.logoutUser()},e.renderLogoSwitch=function(){return s.a.createElement(W,null,s.a.createElement(M.a,{className:"sidenav__toggle show-on-lg",onChange:e.handleSidenavToggle,checked:!e.state.sidenavToggleChecked,color:"secondary"}))},e}return Object(o.a)(a,[{key:"componentWillMount",value:function(){var e=this;this.unlistenRouteChange=this.props.history.listen(function(t,a){Object(h.d)()&&e.updateSidebarMode({mode:"close"})})}},{key:"componentWillUnmount",value:function(){this.unlistenRouteChange()}},{key:"render",value:function(){var e=this.props,t=e.theme,a=e.settings,n=a.themes[a.layout1Settings.leftSidebar.theme]||t;return s.a.createElement(S.a,{theme:n},s.a.createElement(D,{theme:n,settings:a}),s.a.createElement("div",{className:"sidenav"},s.a.createElement("div",{className:"sidenav__hold"},s.a.createElement(l.Fragment,null,this.renderLogoSwitch(),s.a.createElement(U,null)))))}}]),a}(l.Component)),F=Object(b.a)(function(e){return{}},{withTheme:!0})(Object(y.g)(Object(d.b)(function(e){return{setDefaultSettings:m.a.func.isRequired,setLayoutSettings:m.a.func.isRequired,logoutUser:m.a.func.isRequired,user:e.user,settings:e.layout.settings}},{setLayoutSettings:p.d,setDefaultSettings:p.c})(H))),J=a(143),B=function(e){Object(c.a)(a,e);var t=Object(r.a)(a);function a(){var e;Object(i.a)(this,a);for(var o=arguments.length,c=new Array(o),r=0;r<o;r++)c[r]=arguments[r];return(e=t.call.apply(t,[this].concat(c))).updateSidebarMode=function(t){var a=e.props,i=a.settings;(0,a.setLayoutSettings)(Object(n.a)(Object(n.a)({},i),{},{layout1Settings:Object(n.a)(Object(n.a)({},i.layout1Settings),{},{leftSidebar:Object(n.a)(Object(n.a)({},i.layout1Settings.leftSidebar),t)})}))},e}return Object(o.a)(a,[{key:"componentWillMount",value:function(){Object(h.d)()&&this.updateSidebarMode({mode:"close"})}},{key:"componentWillUnmount",value:function(){}},{key:"render",value:function(){var e=this.props,t=e.settings,a=e.classes,n=e.theme,i=t.layout1Settings,o={[a.layout]:!0,["".concat(t.activeLayout," sidenav-").concat(i.leftSidebar.mode," theme-").concat(n.palette.type," flex")]:!0,"topbar-fixed":i.topbar.fixed};return s.a.createElement(J.a.Consumer,null,function(e){var a=e.routes;return s.a.createElement("div",{className:Object(h.a)(o)},i.leftSidebar.show&&s.a.createElement(F,null),s.a.createElement("div",{className:"content-wrap position-relative"},i.topbar.show&&i.topbar.fixed&&s.a.createElement(R,{className:"elevation-z8"}),t.perfectScrollbar&&s.a.createElement(g.a,{className:"scrollable-content"},i.topbar.show&&!i.topbar.fixed&&s.a.createElement(R,{style:{height:"80px"}}),s.a.createElement("div",{className:"content"},Object(v.b)(a)),s.a.createElement("div",{className:"my-auto"})),!t.perfectScrollbar&&s.a.createElement("div",{className:"scrollable-content"},i.topbar.show&&!i.topbar.fixed&&s.a.createElement(R,null),s.a.createElement("div",{className:"content"},Object(v.b)(a)),s.a.createElement("div",{className:"my-auto"}))))})}}]),a}(l.Component);t.default=Object(b.a)(function(e){return{layout:{backgroundColor:e.palette.background.default}}},{withTheme:!0})(Object(d.b)(function(e){return{setLayoutSettings:u.PropTypes.func.isRequired,settings:e.layout.settings}},{setLayoutSettings:p.d})(B))}}]);
//# sourceMappingURL=30.fa9228c7.chunk.js.map