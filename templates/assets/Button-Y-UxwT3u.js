import{k as g,s as wo,l as U,G as uo,R as D,aB as Ho,ar as zo,a6 as Do,a1 as Bo,af as K,t as bo,z as Fo,I as Io,n as E,m as u,o as lo,T as Eo,aj as ao,e as Go,$ as Ro,f as Wo,c as ko,ax as Oo,au as Mo,av as jo,aC as xo,aA as _o,aD as No,u as A,W as Ko,p as Lo,A as t,q as X,r as co}from"./index-7TDlwo0a.js";const J=typeof document<"u"&&typeof window<"u",{cubicBezierEaseInOut:G}=wo;function Qo({duration:e=".2s",delay:y=".1s"}={}){return[g("&.fade-in-width-expand-transition-leave-from, &.fade-in-width-expand-transition-enter-to",{opacity:1}),g("&.fade-in-width-expand-transition-leave-to, &.fade-in-width-expand-transition-enter-from",`
 opacity: 0!important;
 margin-left: 0!important;
 margin-right: 0!important;
 `),g("&.fade-in-width-expand-transition-leave-active",`
 overflow: hidden;
 transition:
 opacity ${e} ${G},
 max-width ${e} ${G} ${y},
 margin-left ${e} ${G} ${y},
 margin-right ${e} ${G} ${y};
 `),g("&.fade-in-width-expand-transition-enter-active",`
 overflow: hidden;
 transition:
 opacity ${e} ${G} ${y},
 max-width ${e} ${G},
 margin-left ${e} ${G},
 margin-right ${e} ${G};
 `)]}const Vo=U("base-wave",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 border-radius: inherit;
`),qo=uo({name:"BaseWave",props:{clsPrefix:{type:String,required:!0}},setup(e){Ho("-base-wave",Vo,zo(e,"clsPrefix"));const y=K(null),m=K(!1);let b=null;return Do(()=>{b!==null&&window.clearTimeout(b)}),{active:m,selfRef:y,play(){b!==null&&(window.clearTimeout(b),m.value=!1,b=null),Bo(()=>{var P;(P=y.value)===null||P===void 0||P.offsetHeight,m.value=!0,b=window.setTimeout(()=>{m.value=!1,b=null},1e3)})}}},render(){const{clsPrefix:e}=this;return D("div",{ref:"selfRef","aria-hidden":!0,class:[`${e}-base-wave`,this.active&&`${e}-base-wave--active`]})}}),Ao=J&&"chrome"in window;J&&navigator.userAgent.includes("Firefox");const Xo=J&&navigator.userAgent.includes("Safari")&&!Ao;function k(e){return bo(e,[255,255,255,.16])}function Y(e){return bo(e,[0,0,0,.12])}const Yo=Fo("n-button-group"),Uo={paddingTiny:"0 6px",paddingSmall:"0 10px",paddingMedium:"0 14px",paddingLarge:"0 18px",paddingRoundTiny:"0 10px",paddingRoundSmall:"0 14px",paddingRoundMedium:"0 18px",paddingRoundLarge:"0 22px",iconMarginTiny:"6px",iconMarginSmall:"6px",iconMarginMedium:"6px",iconMarginLarge:"6px",iconSizeTiny:"14px",iconSizeSmall:"18px",iconSizeMedium:"18px",iconSizeLarge:"20px",rippleDuration:".6s"};function Jo(e){const{heightTiny:y,heightSmall:m,heightMedium:b,heightLarge:P,borderRadius:O,fontSizeTiny:L,fontSizeSmall:M,fontSizeMedium:Z,fontSizeLarge:j,opacityDisabled:_,textColor2:f,textColor3:oo,primaryColorHover:c,primaryColorPressed:B,borderColor:Q,primaryColor:w,baseColor:s,infoColor:F,infoColorHover:H,infoColorPressed:z,successColor:r,successColorHover:i,successColorPressed:v,warningColor:o,warningColorHover:h,warningColorPressed:S,errorColor:p,errorColorHover:$,errorColorPressed:C,fontWeight:N,buttonColor2:I,buttonColor2Hover:R,buttonColor2Pressed:T,fontWeightStrong:l}=e;return Object.assign(Object.assign({},Uo),{heightTiny:y,heightSmall:m,heightMedium:b,heightLarge:P,borderRadiusTiny:O,borderRadiusSmall:O,borderRadiusMedium:O,borderRadiusLarge:O,fontSizeTiny:L,fontSizeSmall:M,fontSizeMedium:Z,fontSizeLarge:j,opacityDisabled:_,colorOpacitySecondary:"0.16",colorOpacitySecondaryHover:"0.22",colorOpacitySecondaryPressed:"0.28",colorSecondary:I,colorSecondaryHover:R,colorSecondaryPressed:T,colorTertiary:I,colorTertiaryHover:R,colorTertiaryPressed:T,colorQuaternary:"#0000",colorQuaternaryHover:R,colorQuaternaryPressed:T,color:"#0000",colorHover:"#0000",colorPressed:"#0000",colorFocus:"#0000",colorDisabled:"#0000",textColor:f,textColorTertiary:oo,textColorHover:c,textColorPressed:B,textColorFocus:c,textColorDisabled:f,textColorText:f,textColorTextHover:c,textColorTextPressed:B,textColorTextFocus:c,textColorTextDisabled:f,textColorGhost:f,textColorGhostHover:c,textColorGhostPressed:B,textColorGhostFocus:c,textColorGhostDisabled:f,border:`1px solid ${Q}`,borderHover:`1px solid ${c}`,borderPressed:`1px solid ${B}`,borderFocus:`1px solid ${c}`,borderDisabled:`1px solid ${Q}`,rippleColor:w,colorPrimary:w,colorHoverPrimary:c,colorPressedPrimary:B,colorFocusPrimary:c,colorDisabledPrimary:w,textColorPrimary:s,textColorHoverPrimary:s,textColorPressedPrimary:s,textColorFocusPrimary:s,textColorDisabledPrimary:s,textColorTextPrimary:w,textColorTextHoverPrimary:c,textColorTextPressedPrimary:B,textColorTextFocusPrimary:c,textColorTextDisabledPrimary:f,textColorGhostPrimary:w,textColorGhostHoverPrimary:c,textColorGhostPressedPrimary:B,textColorGhostFocusPrimary:c,textColorGhostDisabledPrimary:w,borderPrimary:`1px solid ${w}`,borderHoverPrimary:`1px solid ${c}`,borderPressedPrimary:`1px solid ${B}`,borderFocusPrimary:`1px solid ${c}`,borderDisabledPrimary:`1px solid ${w}`,rippleColorPrimary:w,colorInfo:F,colorHoverInfo:H,colorPressedInfo:z,colorFocusInfo:H,colorDisabledInfo:F,textColorInfo:s,textColorHoverInfo:s,textColorPressedInfo:s,textColorFocusInfo:s,textColorDisabledInfo:s,textColorTextInfo:F,textColorTextHoverInfo:H,textColorTextPressedInfo:z,textColorTextFocusInfo:H,textColorTextDisabledInfo:f,textColorGhostInfo:F,textColorGhostHoverInfo:H,textColorGhostPressedInfo:z,textColorGhostFocusInfo:H,textColorGhostDisabledInfo:F,borderInfo:`1px solid ${F}`,borderHoverInfo:`1px solid ${H}`,borderPressedInfo:`1px solid ${z}`,borderFocusInfo:`1px solid ${H}`,borderDisabledInfo:`1px solid ${F}`,rippleColorInfo:F,colorSuccess:r,colorHoverSuccess:i,colorPressedSuccess:v,colorFocusSuccess:i,colorDisabledSuccess:r,textColorSuccess:s,textColorHoverSuccess:s,textColorPressedSuccess:s,textColorFocusSuccess:s,textColorDisabledSuccess:s,textColorTextSuccess:r,textColorTextHoverSuccess:i,textColorTextPressedSuccess:v,textColorTextFocusSuccess:i,textColorTextDisabledSuccess:f,textColorGhostSuccess:r,textColorGhostHoverSuccess:i,textColorGhostPressedSuccess:v,textColorGhostFocusSuccess:i,textColorGhostDisabledSuccess:r,borderSuccess:`1px solid ${r}`,borderHoverSuccess:`1px solid ${i}`,borderPressedSuccess:`1px solid ${v}`,borderFocusSuccess:`1px solid ${i}`,borderDisabledSuccess:`1px solid ${r}`,rippleColorSuccess:r,colorWarning:o,colorHoverWarning:h,colorPressedWarning:S,colorFocusWarning:h,colorDisabledWarning:o,textColorWarning:s,textColorHoverWarning:s,textColorPressedWarning:s,textColorFocusWarning:s,textColorDisabledWarning:s,textColorTextWarning:o,textColorTextHoverWarning:h,textColorTextPressedWarning:S,textColorTextFocusWarning:h,textColorTextDisabledWarning:f,textColorGhostWarning:o,textColorGhostHoverWarning:h,textColorGhostPressedWarning:S,textColorGhostFocusWarning:h,textColorGhostDisabledWarning:o,borderWarning:`1px solid ${o}`,borderHoverWarning:`1px solid ${h}`,borderPressedWarning:`1px solid ${S}`,borderFocusWarning:`1px solid ${h}`,borderDisabledWarning:`1px solid ${o}`,rippleColorWarning:o,colorError:p,colorHoverError:$,colorPressedError:C,colorFocusError:$,colorDisabledError:p,textColorError:s,textColorHoverError:s,textColorPressedError:s,textColorFocusError:s,textColorDisabledError:s,textColorTextError:p,textColorTextHoverError:$,textColorTextPressedError:C,textColorTextFocusError:$,textColorTextDisabledError:f,textColorGhostError:p,textColorGhostHoverError:$,textColorGhostPressedError:C,textColorGhostFocusError:$,textColorGhostDisabledError:p,borderError:`1px solid ${p}`,borderHoverError:`1px solid ${$}`,borderPressedError:`1px solid ${C}`,borderFocusError:`1px solid ${$}`,borderDisabledError:`1px solid ${p}`,rippleColorError:p,waveOpacity:"0.6",fontWeight:N,fontWeightStrong:l})}const Zo={name:"Button",common:Io,self:Jo},oe=g([U("button",`
 margin: 0;
 font-weight: var(--n-font-weight);
 line-height: 1;
 font-family: inherit;
 padding: var(--n-padding);
 height: var(--n-height);
 font-size: var(--n-font-size);
 border-radius: var(--n-border-radius);
 color: var(--n-text-color);
 background-color: var(--n-color);
 width: var(--n-width);
 white-space: nowrap;
 outline: none;
 position: relative;
 z-index: auto;
 border: none;
 display: inline-flex;
 flex-wrap: nowrap;
 flex-shrink: 0;
 align-items: center;
 justify-content: center;
 user-select: none;
 -webkit-user-select: none;
 text-align: center;
 cursor: pointer;
 text-decoration: none;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 opacity .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[E("color",[u("border",{borderColor:"var(--n-border-color)"}),E("disabled",[u("border",{borderColor:"var(--n-border-color-disabled)"})]),lo("disabled",[g("&:focus",[u("state-border",{borderColor:"var(--n-border-color-focus)"})]),g("&:hover",[u("state-border",{borderColor:"var(--n-border-color-hover)"})]),g("&:active",[u("state-border",{borderColor:"var(--n-border-color-pressed)"})]),E("pressed",[u("state-border",{borderColor:"var(--n-border-color-pressed)"})])])]),E("disabled",{backgroundColor:"var(--n-color-disabled)",color:"var(--n-text-color-disabled)"},[u("border",{border:"var(--n-border-disabled)"})]),lo("disabled",[g("&:focus",{backgroundColor:"var(--n-color-focus)",color:"var(--n-text-color-focus)"},[u("state-border",{border:"var(--n-border-focus)"})]),g("&:hover",{backgroundColor:"var(--n-color-hover)",color:"var(--n-text-color-hover)"},[u("state-border",{border:"var(--n-border-hover)"})]),g("&:active",{backgroundColor:"var(--n-color-pressed)",color:"var(--n-text-color-pressed)"},[u("state-border",{border:"var(--n-border-pressed)"})]),E("pressed",{backgroundColor:"var(--n-color-pressed)",color:"var(--n-text-color-pressed)"},[u("state-border",{border:"var(--n-border-pressed)"})])]),E("loading","cursor: wait;"),U("base-wave",`
 pointer-events: none;
 top: 0;
 right: 0;
 bottom: 0;
 left: 0;
 animation-iteration-count: 1;
 animation-duration: var(--n-ripple-duration);
 animation-timing-function: var(--n-bezier-ease-out), var(--n-bezier-ease-out);
 `,[E("active",{zIndex:1,animationName:"button-wave-spread, button-wave-opacity"})]),J&&"MozBoxSizing"in document.createElement("div").style?g("&::moz-focus-inner",{border:0}):null,u("border, state-border",`
 position: absolute;
 left: 0;
 top: 0;
 right: 0;
 bottom: 0;
 border-radius: inherit;
 transition: border-color .3s var(--n-bezier);
 pointer-events: none;
 `),u("border",`
 border: var(--n-border);
 `),u("state-border",`
 border: var(--n-border);
 border-color: #0000;
 z-index: 1;
 `),u("icon",`
 margin: var(--n-icon-margin);
 margin-left: 0;
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 max-width: var(--n-icon-size);
 font-size: var(--n-icon-size);
 position: relative;
 flex-shrink: 0;
 `,[U("icon-slot",`
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 position: absolute;
 left: 0;
 top: 50%;
 transform: translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `,[Eo({top:"50%",originalTransform:"translateY(-50%)"})]),Qo()]),u("content",`
 display: flex;
 align-items: center;
 flex-wrap: nowrap;
 min-width: 0;
 `,[g("~",[u("icon",{margin:"var(--n-icon-margin)",marginRight:0})])]),E("block",`
 display: flex;
 width: 100%;
 `),E("dashed",[u("border, state-border",{borderStyle:"dashed !important"})]),E("disabled",{cursor:"not-allowed",opacity:"var(--n-opacity-disabled)"})]),g("@keyframes button-wave-spread",{from:{boxShadow:"0 0 0.5px 0 var(--n-ripple-color)"},to:{boxShadow:"0 0 0.5px 4.5px var(--n-ripple-color)"}}),g("@keyframes button-wave-opacity",{from:{opacity:"var(--n-wave-opacity)"},to:{opacity:0}})]),ee=Object.assign(Object.assign({},xo.props),{color:String,textColor:String,text:Boolean,block:Boolean,loading:Boolean,disabled:Boolean,circle:Boolean,size:String,ghost:Boolean,round:Boolean,secondary:Boolean,tertiary:Boolean,quaternary:Boolean,strong:Boolean,focusable:{type:Boolean,default:!0},keyboard:{type:Boolean,default:!0},tag:{type:String,default:"button"},type:{type:String,default:"default"},dashed:Boolean,renderIcon:Function,iconPlacement:{type:String,default:"left"},attrType:{type:String,default:"button"},bordered:{type:Boolean,default:!0},onClick:[Function,Array],nativeFocusBehavior:{type:Boolean,default:!Xo},spinProps:Object}),re=uo({name:"Button",props:ee,slots:Object,setup(e){const y=K(null),m=K(null),b=K(!1),P=Oo(()=>!e.quaternary&&!e.tertiary&&!e.secondary&&!e.text&&(!e.color||e.ghost||e.dashed)&&e.bordered),O=Ko(Yo,{}),{inlineThemeDisabled:L,mergedClsPrefixRef:M,mergedRtlRef:Z,mergedComponentPropsRef:j}=Mo(e),{mergedSizeRef:_}=jo({},{defaultSize:"medium",mergedSize:r=>{var i,v;const{size:o}=e;if(o)return o;const{size:h}=O;if(h)return h;const{mergedSize:S}=r||{};if(S)return S.value;const p=(v=(i=j==null?void 0:j.value)===null||i===void 0?void 0:i.Button)===null||v===void 0?void 0:v.size;return p||"medium"}}),f=A(()=>e.focusable&&!e.disabled),oo=r=>{var i;f.value||r.preventDefault(),!e.nativeFocusBehavior&&(r.preventDefault(),!e.disabled&&f.value&&((i=y.value)===null||i===void 0||i.focus({preventScroll:!0})))},c=r=>{var i;if(!e.disabled&&!e.loading){const{onClick:v}=e;v&&Lo(v,r),e.text||(i=m.value)===null||i===void 0||i.play()}},B=r=>{switch(r.key){case"Enter":if(!e.keyboard)return;b.value=!1}},Q=r=>{switch(r.key){case"Enter":if(!e.keyboard||e.loading){r.preventDefault();return}b.value=!0}},w=()=>{b.value=!1},s=xo("Button","-button",oe,Zo,e,M),F=_o("Button",Z,M),H=A(()=>{const r=s.value,{common:{cubicBezierEaseInOut:i,cubicBezierEaseOut:v},self:o}=r,{rippleDuration:h,opacityDisabled:S,fontWeight:p,fontWeightStrong:$}=o,C=_.value,{dashed:N,type:I,ghost:R,text:T,color:l,round:no,circle:eo,textColor:W,secondary:fo,tertiary:so,quaternary:vo,strong:ho}=e,po={"--n-font-weight":ho?$:p};let a={"--n-color":"initial","--n-color-hover":"initial","--n-color-pressed":"initial","--n-color-focus":"initial","--n-color-disabled":"initial","--n-ripple-color":"initial","--n-text-color":"initial","--n-text-color-hover":"initial","--n-text-color-pressed":"initial","--n-text-color-focus":"initial","--n-text-color-disabled":"initial"};const V=I==="tertiary",io=I==="default",n=V?"default":I;if(T){const d=W||l;a={"--n-color":"#0000","--n-color-hover":"#0000","--n-color-pressed":"#0000","--n-color-focus":"#0000","--n-color-disabled":"#0000","--n-ripple-color":"#0000","--n-text-color":d||o[t("textColorText",n)],"--n-text-color-hover":d?k(d):o[t("textColorTextHover",n)],"--n-text-color-pressed":d?Y(d):o[t("textColorTextPressed",n)],"--n-text-color-focus":d?k(d):o[t("textColorTextHover",n)],"--n-text-color-disabled":d||o[t("textColorTextDisabled",n)]}}else if(R||N){const d=W||l;a={"--n-color":"#0000","--n-color-hover":"#0000","--n-color-pressed":"#0000","--n-color-focus":"#0000","--n-color-disabled":"#0000","--n-ripple-color":l||o[t("rippleColor",n)],"--n-text-color":d||o[t("textColorGhost",n)],"--n-text-color-hover":d?k(d):o[t("textColorGhostHover",n)],"--n-text-color-pressed":d?Y(d):o[t("textColorGhostPressed",n)],"--n-text-color-focus":d?k(d):o[t("textColorGhostHover",n)],"--n-text-color-disabled":d||o[t("textColorGhostDisabled",n)]}}else if(fo){const d=io?o.textColor:V?o.textColorTertiary:o[t("color",n)],x=l||d,q=I!=="default"&&I!=="tertiary";a={"--n-color":q?X(x,{alpha:Number(o.colorOpacitySecondary)}):o.colorSecondary,"--n-color-hover":q?X(x,{alpha:Number(o.colorOpacitySecondaryHover)}):o.colorSecondaryHover,"--n-color-pressed":q?X(x,{alpha:Number(o.colorOpacitySecondaryPressed)}):o.colorSecondaryPressed,"--n-color-focus":q?X(x,{alpha:Number(o.colorOpacitySecondaryHover)}):o.colorSecondaryHover,"--n-color-disabled":o.colorSecondary,"--n-ripple-color":"#0000","--n-text-color":x,"--n-text-color-hover":x,"--n-text-color-pressed":x,"--n-text-color-focus":x,"--n-text-color-disabled":x}}else if(so||vo){const d=io?o.textColor:V?o.textColorTertiary:o[t("color",n)],x=l||d;so?(a["--n-color"]=o.colorTertiary,a["--n-color-hover"]=o.colorTertiaryHover,a["--n-color-pressed"]=o.colorTertiaryPressed,a["--n-color-focus"]=o.colorSecondaryHover,a["--n-color-disabled"]=o.colorTertiary):(a["--n-color"]=o.colorQuaternary,a["--n-color-hover"]=o.colorQuaternaryHover,a["--n-color-pressed"]=o.colorQuaternaryPressed,a["--n-color-focus"]=o.colorQuaternaryHover,a["--n-color-disabled"]=o.colorQuaternary),a["--n-ripple-color"]="#0000",a["--n-text-color"]=x,a["--n-text-color-hover"]=x,a["--n-text-color-pressed"]=x,a["--n-text-color-focus"]=x,a["--n-text-color-disabled"]=x}else a={"--n-color":l||o[t("color",n)],"--n-color-hover":l?k(l):o[t("colorHover",n)],"--n-color-pressed":l?Y(l):o[t("colorPressed",n)],"--n-color-focus":l?k(l):o[t("colorFocus",n)],"--n-color-disabled":l||o[t("colorDisabled",n)],"--n-ripple-color":l||o[t("rippleColor",n)],"--n-text-color":W||(l?o.textColorPrimary:V?o.textColorTertiary:o[t("textColor",n)]),"--n-text-color-hover":W||(l?o.textColorHoverPrimary:o[t("textColorHover",n)]),"--n-text-color-pressed":W||(l?o.textColorPressedPrimary:o[t("textColorPressed",n)]),"--n-text-color-focus":W||(l?o.textColorFocusPrimary:o[t("textColorFocus",n)]),"--n-text-color-disabled":W||(l?o.textColorDisabledPrimary:o[t("textColorDisabled",n)])};let ro={"--n-border":"initial","--n-border-hover":"initial","--n-border-pressed":"initial","--n-border-focus":"initial","--n-border-disabled":"initial"};T?ro={"--n-border":"none","--n-border-hover":"none","--n-border-pressed":"none","--n-border-focus":"none","--n-border-disabled":"none"}:ro={"--n-border":o[t("border",n)],"--n-border-hover":o[t("borderHover",n)],"--n-border-pressed":o[t("borderPressed",n)],"--n-border-focus":o[t("borderFocus",n)],"--n-border-disabled":o[t("borderDisabled",n)]};const{[t("height",C)]:to,[t("fontSize",C)]:Co,[t("padding",C)]:go,[t("paddingRound",C)]:yo,[t("iconSize",C)]:mo,[t("borderRadius",C)]:Po,[t("iconMargin",C)]:So,waveOpacity:$o}=o,To={"--n-width":eo&&!T?to:"initial","--n-height":T?"initial":to,"--n-font-size":Co,"--n-padding":eo||T?"initial":no?yo:go,"--n-icon-size":mo,"--n-icon-margin":So,"--n-border-radius":T?"initial":eo||no?to:Po};return Object.assign(Object.assign(Object.assign(Object.assign({"--n-bezier":i,"--n-bezier-ease-out":v,"--n-ripple-duration":h,"--n-opacity-disabled":S,"--n-wave-opacity":$o},po),a),ro),To)}),z=L?No("button",A(()=>{let r="";const{dashed:i,type:v,ghost:o,text:h,color:S,round:p,circle:$,textColor:C,secondary:N,tertiary:I,quaternary:R,strong:T}=e;i&&(r+="a"),o&&(r+="b"),h&&(r+="c"),p&&(r+="d"),$&&(r+="e"),N&&(r+="f"),I&&(r+="g"),R&&(r+="h"),T&&(r+="i"),S&&(r+=`j${co(S)}`),C&&(r+=`k${co(C)}`);const{value:l}=_;return r+=`l${l[0]}`,r+=`m${v[0]}`,r}),H,e):void 0;return{selfElRef:y,waveElRef:m,mergedClsPrefix:M,mergedFocusable:f,mergedSize:_,showBorder:P,enterPressed:b,rtlEnabled:F,handleMousedown:oo,handleKeydown:Q,handleBlur:w,handleKeyup:B,handleClick:c,customColorCssVars:A(()=>{const{color:r}=e;if(!r)return null;const i=k(r);return{"--n-border-color":r,"--n-border-color-hover":i,"--n-border-color-pressed":Y(r),"--n-border-color-focus":i,"--n-border-color-disabled":r}}),cssVars:L?void 0:H,themeClass:z==null?void 0:z.themeClass,onRender:z==null?void 0:z.onRender}},render(){const{mergedClsPrefix:e,tag:y,onRender:m}=this;m==null||m();const b=ao(this.$slots.default,P=>P&&D("span",{class:`${e}-button__content`},P));return D(y,{ref:"selfElRef",class:[this.themeClass,`${e}-button`,`${e}-button--${this.type}-type`,`${e}-button--${this.mergedSize}-type`,this.rtlEnabled&&`${e}-button--rtl`,this.disabled&&`${e}-button--disabled`,this.block&&`${e}-button--block`,this.enterPressed&&`${e}-button--pressed`,!this.text&&this.dashed&&`${e}-button--dashed`,this.color&&`${e}-button--color`,this.secondary&&`${e}-button--secondary`,this.loading&&`${e}-button--loading`,this.ghost&&`${e}-button--ghost`],tabindex:this.mergedFocusable?0:-1,type:this.attrType,style:this.cssVars,disabled:this.disabled,onClick:this.handleClick,onBlur:this.handleBlur,onMousedown:this.handleMousedown,onKeyup:this.handleKeyup,onKeydown:this.handleKeydown},this.iconPlacement==="right"&&b,D(Go,{width:!0},{default:()=>ao(this.$slots.icon,P=>(this.loading||this.renderIcon||P)&&D("span",{class:`${e}-button__icon`,style:{margin:Ro(this.$slots.default)?"0":""}},D(Wo,null,{default:()=>this.loading?D(ko,Object.assign({clsPrefix:e,key:"loading",class:`${e}-icon-slot`,strokeWidth:20},this.spinProps)):D("div",{key:"icon",class:`${e}-icon-slot`,role:"none"},this.renderIcon?this.renderIcon():P)})))}),this.iconPlacement==="left"&&b,this.text?null:D(qo,{ref:"waveElRef",clsPrefix:e}),this.showBorder?D("div",{"aria-hidden":!0,class:`${e}-button__border`,style:this.customColorCssVars}):null,this.showBorder?D("div",{"aria-hidden":!0,class:`${e}-button__state-border`,style:this.customColorCssVars}):null)}}),ne=re;export{re as B,ne as X,Xo as a,Zo as b,J as i};
