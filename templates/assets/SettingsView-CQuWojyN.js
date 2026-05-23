import{E as se,Q as p,H as Ee,j as f,k as z,i as Qe,m as M,l as O,U as qe,W as Ye,ah as D,as as De,aA as ve,ay as Ae,aB as Ze,I as G,S as eo,a as oo,o as K,t as T,z as Ve,P as to,B as no,au as ro,at as lo,ad as A,aw as ao,av as J,aC as io,af as Ne,b as Oe,$ as so,a3 as ke,ai as uo,ap as co,a5 as fo,J as vo,K as mo,a4 as po,x as le,v as d,D as V,aE as X,ar as S,ax as go,ac as bo,a7 as ae,g as ie,X as Ie,F as ho,ae as xo,a1 as yo,ao as So,A as Re,a8 as Co,_ as wo}from"./index-CoNKvCnm.js";import{b as zo,X as Pe,B as Me}from"./Button-CxmD6HPx.js";import{i as Vo,N as Q,a as Io}from"./Switch-Bn5rUsiN.js";import{u as _o}from"./use-message-D-uqPleS.js";const Bo=se({name:"Add",render(){return p("svg",{width:"512",height:"512",viewBox:"0 0 512 512",fill:"none",xmlns:"http://www.w3.org/2000/svg"},p("path",{d:"M256 112V400M400 256H112",stroke:"currentColor","stroke-width":"32","stroke-linecap":"round","stroke-linejoin":"round"}))}}),No=se({name:"Remove",render(){return p("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 512 512"},p("line",{x1:"400",y1:"256",x2:"112",y2:"256",style:`
        fill: none;
        stroke: currentColor;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-width: 32px;
      `}))}}),Oo={paddingSmall:"12px 16px 12px",paddingMedium:"19px 24px 20px",paddingLarge:"23px 32px 24px",paddingHuge:"27px 40px 28px",titleFontSizeSmall:"16px",titleFontSizeMedium:"18px",titleFontSizeLarge:"18px",titleFontSizeHuge:"18px",closeIconSize:"18px",closeSize:"22px"};function ko(e){const{primaryColor:v,borderRadius:w,lineHeight:a,fontSize:m,cardColor:g,textColor2:u,textColor1:B,dividerColor:I,fontWeightStrong:C,closeIconColor:i,closeIconColorHover:s,closeIconColorPressed:_,closeColorHover:F,closeColorPressed:$,modalColor:j,boxShadow1:h,popoverColor:k,actionColor:R}=e;return Object.assign(Object.assign({},Oo),{lineHeight:a,color:g,colorModal:j,colorPopover:k,colorTarget:v,colorEmbedded:R,colorEmbeddedModal:R,colorEmbeddedPopover:R,textColor:u,titleTextColor:B,borderColor:I,actionColor:R,titleFontWeight:C,closeColorHover:F,closeColorPressed:$,closeBorderRadius:w,closeIconColor:i,closeIconColorHover:s,closeIconColorPressed:_,fontSizeSmall:m,fontSizeMedium:m,fontSizeLarge:m,fontSizeHuge:m,boxShadow:h,borderRadius:w})}const Ro={common:Ee,self:ko},Fe=z("card-content",`
 flex: 1;
 min-width: 0;
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
`),Po=f([z("card",`
 font-size: var(--n-font-size);
 line-height: var(--n-line-height);
 display: flex;
 flex-direction: column;
 width: 100%;
 box-sizing: border-box;
 position: relative;
 border-radius: var(--n-border-radius);
 background-color: var(--n-color);
 color: var(--n-text-color);
 word-break: break-word;
 transition: 
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[Qe({background:"var(--n-color-modal)"}),M("hoverable",[f("&:hover","box-shadow: var(--n-box-shadow);")]),M("content-segmented",[f(">",[z("card-content",`
 padding-top: var(--n-padding-bottom);
 `),O("content-scrollbar",[f(">",[z("scrollbar-container",[f(">",[z("card-content",`
 padding-top: var(--n-padding-bottom);
 `)])])])])])]),M("content-soft-segmented",[f(">",[z("card-content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `),O("content-scrollbar",[f(">",[z("scrollbar-container",[f(">",[z("card-content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `)])])])])])]),M("footer-segmented",[f(">",[O("footer",`
 padding-top: var(--n-padding-bottom);
 `)])]),M("footer-soft-segmented",[f(">",[O("footer",`
 padding: var(--n-padding-bottom) 0;
 margin: 0 var(--n-padding-left);
 `)])]),f(">",[z("card-header",`
 box-sizing: border-box;
 display: flex;
 align-items: center;
 font-size: var(--n-title-font-size);
 padding:
 var(--n-padding-top)
 var(--n-padding-left)
 var(--n-padding-bottom)
 var(--n-padding-left);
 `,[O("main",`
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 flex: 1;
 min-width: 0;
 color: var(--n-title-text-color);
 `),O("extra",`
 display: flex;
 align-items: center;
 font-size: var(--n-font-size);
 font-weight: 400;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 `),O("close",`
 margin: 0 0 0 8px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `)]),O("action",`
 box-sizing: border-box;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 background-clip: padding-box;
 background-color: var(--n-action-color);
 `),Fe,z("card-content",[f("&:first-child",`
 padding-top: var(--n-padding-bottom);
 `)]),O("content-scrollbar",`
 display: flex;
 flex-direction: column;
 `,[f(">",[z("scrollbar-container",[f(">",[Fe])])]),f("&:first-child >",[z("scrollbar-container",[f(">",[z("card-content",`
 padding-top: var(--n-padding-bottom);
 `)])])])]),O("footer",`
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
 `,[f("&:first-child",`
 padding-top: var(--n-padding-bottom);
 `)]),O("action",`
 background-color: var(--n-action-color);
 padding: var(--n-padding-bottom) var(--n-padding-left);
 border-bottom-left-radius: var(--n-border-radius);
 border-bottom-right-radius: var(--n-border-radius);
 `)]),z("card-cover",`
 overflow: hidden;
 width: 100%;
 border-radius: var(--n-border-radius) var(--n-border-radius) 0 0;
 `,[f("img",`
 display: block;
 width: 100%;
 `)]),M("bordered",`
 border: 1px solid var(--n-border-color);
 `,[f("&:target","border-color: var(--n-color-target);")]),M("action-segmented",[f(">",[O("action",[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),M("content-segmented, content-soft-segmented",[f(">",[z("card-content",`
 transition: border-color 0.3s var(--n-bezier);
 `,[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)]),O("content-scrollbar",`
 transition: border-color 0.3s var(--n-bezier);
 `,[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),M("footer-segmented, footer-soft-segmented",[f(">",[O("footer",`
 transition: border-color 0.3s var(--n-bezier);
 `,[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),M("embedded",`
 background-color: var(--n-color-embedded);
 `)]),qe(z("card",`
 background: var(--n-color-modal);
 `,[M("embedded",`
 background-color: var(--n-color-embedded-modal);
 `)])),Ye(z("card",`
 background: var(--n-color-popover);
 `,[M("embedded",`
 background-color: var(--n-color-embedded-popover);
 `)]))]),Mo={title:[String,Function],contentClass:String,contentStyle:[Object,String],contentScrollable:Boolean,headerClass:String,headerStyle:[Object,String],headerExtraClass:String,headerExtraStyle:[Object,String],footerClass:String,footerStyle:[Object,String],embedded:Boolean,segmented:{type:[Boolean,Object],default:!1},size:String,bordered:{type:Boolean,default:!0},closable:Boolean,hoverable:Boolean,role:String,onClose:[Function,Array],tag:{type:String,default:"div"},cover:Function,content:[String,Function],footer:Function,action:Function,headerExtra:Function,closeFocusable:Boolean},Fo=Object.assign(Object.assign({},ve.props),Mo),fe=se({name:"Card",props:Fo,slots:Object,setup(e){const v=()=>{const{onClose:s}=e;s&&K(s)},{inlineThemeDisabled:w,mergedClsPrefixRef:a,mergedRtlRef:m,mergedComponentPropsRef:g}=De(e),u=ve("Card","-card",Po,Ro,e,a),B=Ae("Card",m,a),I=T(()=>{var s,_;return e.size||((_=(s=g==null?void 0:g.value)===null||s===void 0?void 0:s.Card)===null||_===void 0?void 0:_.size)||"medium"}),C=T(()=>{const s=I.value,{self:{color:_,colorModal:F,colorTarget:$,textColor:j,titleTextColor:h,titleFontWeight:k,borderColor:R,actionColor:q,borderRadius:Y,lineHeight:U,closeIconColor:c,closeIconColorHover:t,closeIconColorPressed:r,closeColorHover:x,closeColorPressed:y,closeBorderRadius:Z,closeIconSize:ee,closeSize:oe,boxShadow:me,colorPopover:pe,colorEmbedded:ge,colorEmbeddedModal:te,colorEmbeddedPopover:ne,[Ve("padding",s)]:be,[Ve("fontSize",s)]:he,[Ve("titleFontSize",s)]:de},common:{cubicBezierEaseInOut:xe}}=u.value,{top:ye,left:H,bottom:L}=to(be);return{"--n-bezier":xe,"--n-border-radius":Y,"--n-color":_,"--n-color-modal":F,"--n-color-popover":pe,"--n-color-embedded":ge,"--n-color-embedded-modal":te,"--n-color-embedded-popover":ne,"--n-color-target":$,"--n-text-color":j,"--n-line-height":U,"--n-action-color":q,"--n-title-text-color":h,"--n-title-font-weight":k,"--n-close-icon-color":c,"--n-close-icon-color-hover":t,"--n-close-icon-color-pressed":r,"--n-close-color-hover":x,"--n-close-color-pressed":y,"--n-border-color":R,"--n-box-shadow":me,"--n-padding-top":ye,"--n-padding-bottom":L,"--n-padding-left":H,"--n-font-size":he,"--n-title-font-size":de,"--n-close-size":oe,"--n-close-icon-size":ee,"--n-close-border-radius":Z}}),i=w?Ze("card",T(()=>I.value[0]),C,e):void 0;return{rtlEnabled:B,mergedClsPrefix:a,mergedTheme:u,handleCloseClick:v,cssVars:w?void 0:C,themeClass:i==null?void 0:i.themeClass,onRender:i==null?void 0:i.onRender}},render(){const{segmented:e,bordered:v,hoverable:w,mergedClsPrefix:a,rtlEnabled:m,onRender:g,embedded:u,tag:B,$slots:I}=this;return g==null||g(),p(B,{class:[`${a}-card`,this.themeClass,u&&`${a}-card--embedded`,{[`${a}-card--rtl`]:m,[`${a}-card--content-scrollable`]:this.contentScrollable,[`${a}-card--content${typeof e!="boolean"&&e.content==="soft"?"-soft":""}-segmented`]:e===!0||e!==!1&&e.content,[`${a}-card--footer${typeof e!="boolean"&&e.footer==="soft"?"-soft":""}-segmented`]:e===!0||e!==!1&&e.footer,[`${a}-card--action-segmented`]:e===!0||e!==!1&&e.action,[`${a}-card--bordered`]:v,[`${a}-card--hoverable`]:w}],style:this.cssVars,role:this.role},D(I.cover,C=>{const i=this.cover?G([this.cover()]):C;return i&&p("div",{class:`${a}-card-cover`,role:"none"},i)}),D(I.header,C=>{const{title:i}=this,s=i?G(typeof i=="function"?[i()]:[i]):C;return s||this.closable?p("div",{class:[`${a}-card-header`,this.headerClass],style:this.headerStyle,role:"heading"},p("div",{class:`${a}-card-header__main`,role:"heading"},s),D(I["header-extra"],_=>{const F=this.headerExtra?G([this.headerExtra()]):_;return F&&p("div",{class:[`${a}-card-header__extra`,this.headerExtraClass],style:this.headerExtraStyle},F)}),this.closable&&p(oo,{clsPrefix:a,class:`${a}-card-header__close`,onClick:this.handleCloseClick,focusable:this.closeFocusable,absolute:!0})):null}),D(I.default,C=>{const{content:i}=this,s=i?G(typeof i=="function"?[i()]:[i]):C;return s?this.contentScrollable?p(eo,{class:`${a}-card__content-scrollbar`,contentClass:[`${a}-card-content`,this.contentClass],contentStyle:this.contentStyle},s):p("div",{class:[`${a}-card-content`,this.contentClass],style:this.contentStyle,role:"none"},s):null}),D(I.footer,C=>{const i=this.footer?G([this.footer()]):C;return i&&p("div",{class:[`${a}-card__footer`,this.footerClass],style:this.footerStyle,role:"none"},i)}),D(I.action,C=>{const i=this.action?G([this.action()]):C;return i&&p("div",{class:`${a}-card__action`,role:"none"},i)}))}});function To(e){const{textColorDisabled:v}=e;return{iconColorDisabled:v}}const $o=no({name:"InputNumber",common:Ee,peers:{Button:zo,Input:Vo},self:To}),Uo=f([z("input-number-suffix",`
 display: inline-block;
 margin-right: 10px;
 `),z("input-number-prefix",`
 display: inline-block;
 margin-left: 10px;
 `)]);function Eo(e){return e==null||typeof e=="string"&&e.trim()===""?null:Number(e)}function Do(e){return e.includes(".")&&(/^(-)?\d+.*(\.|0)$/.test(e)||/^-?\d*$/.test(e))||e==="-"||e==="-0"}function _e(e){return e==null?!0:!Number.isNaN(e)}function Te(e,v){return typeof e!="number"?"":v===void 0?String(e):e.toFixed(v)}function Be(e){if(e===null)return null;if(typeof e=="number")return e;{const v=Number(e);return Number.isNaN(v)?null:v}}const $e=800,Ue=100,Ao=Object.assign(Object.assign({},ve.props),{autofocus:Boolean,loading:{type:Boolean,default:void 0},placeholder:String,defaultValue:{type:Number,default:null},value:Number,step:{type:[Number,String],default:1},min:[Number,String],max:[Number,String],size:String,disabled:{type:Boolean,default:void 0},validator:Function,bordered:{type:Boolean,default:void 0},showButton:{type:Boolean,default:!0},buttonPlacement:{type:String,default:"right"},inputProps:Object,readonly:Boolean,clearable:Boolean,keyboard:{type:Object,default:{}},updateValueOnInput:{type:Boolean,default:!0},round:{type:Boolean,default:void 0},parse:Function,format:Function,precision:Number,status:String,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onFocus:[Function,Array],onBlur:[Function,Array],onClear:[Function,Array],onChange:[Function,Array]}),jo=se({name:"InputNumber",props:Ao,slots:Object,setup(e){const{mergedBorderedRef:v,mergedClsPrefixRef:w,mergedRtlRef:a,mergedComponentPropsRef:m}=De(e),g=ve("InputNumber","-input-number",Uo,$o,e,w),{localeRef:u}=ro("InputNumber"),B=lo(e,{mergedSize:o=>{var n,l;const{size:b}=e;if(b)return b;const{mergedSize:N}=o||{};if(N!=null&&N.value)return N.value;const P=(l=(n=m==null?void 0:m.value)===null||n===void 0?void 0:n.InputNumber)===null||l===void 0?void 0:l.size;return P||"medium"}}),{mergedSizeRef:I,mergedDisabledRef:C,mergedStatusRef:i}=B,s=A(null),_=A(null),F=A(null),$=A(e.defaultValue),j=co(e,"value"),h=ao(j,$),k=A(""),R=o=>{const n=String(o).split(".")[1];return n?n.length:0},q=o=>{const n=[e.min,e.max,e.step,o].map(l=>l===void 0?0:R(l));return Math.max(...n)},Y=J(()=>{const{placeholder:o}=e;return o!==void 0?o:u.value.placeholder}),U=J(()=>{const o=Be(e.step);return o!==null?o===0?1:Math.abs(o):1}),c=J(()=>{const o=Be(e.min);return o!==null?o:null}),t=J(()=>{const o=Be(e.max);return o!==null?o:null}),r=()=>{const{value:o}=h;if(_e(o)){const{format:n,precision:l}=e;n?k.value=n(o):o===null||l===void 0||R(o)>l?k.value=Te(o,void 0):k.value=Te(o,l)}else k.value=String(o)};r();const x=o=>{const{value:n}=h;if(o===n){r();return}const{"onUpdate:value":l,onUpdateValue:b,onChange:N}=e,{nTriggerFormInput:P,nTriggerFormChange:W}=B;N&&K(N,o),b&&K(b,o),l&&K(l,o),$.value=o,P(),W()},y=({offset:o,doUpdateIfValid:n,fixPrecision:l,isInputing:b})=>{const{value:N}=k;if(b&&Do(N))return!1;const P=(e.parse||Eo)(N);if(P===null)return n&&x(null),null;if(_e(P)){const W=R(P),{precision:re}=e;if(re!==void 0&&re<W&&!l)return!1;let E=Number.parseFloat((P+o).toFixed(re??q(P)));if(_e(E)){const{value:we}=t,{value:ze}=c;if(we!==null&&E>we){if(!n||b)return!1;E=we}if(ze!==null&&E<ze){if(!n||b)return!1;E=ze}return e.validator&&!e.validator(E)?!1:(n&&x(E),E)}}return!1},Z=J(()=>y({offset:0,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})===!1),ee=J(()=>{const{value:o}=h;if(e.validator&&o===null)return!1;const{value:n}=U;return y({offset:-n,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})!==!1}),oe=J(()=>{const{value:o}=h;if(e.validator&&o===null)return!1;const{value:n}=U;return y({offset:+n,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})!==!1});function me(o){const{onFocus:n}=e,{nTriggerFormFocus:l}=B;n&&K(n,o),l()}function pe(o){var n,l;if(o.target===((n=s.value)===null||n===void 0?void 0:n.wrapperElRef))return;const b=y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0});if(b!==!1){const W=(l=s.value)===null||l===void 0?void 0:l.inputElRef;W&&(W.value=String(b||"")),h.value===b&&r()}else r();const{onBlur:N}=e,{nTriggerFormBlur:P}=B;N&&K(N,o),P(),so(()=>{r()})}function ge(o){const{onClear:n}=e;n&&K(n,o)}function te(){const{value:o}=oe;if(!o){Ce();return}const{value:n}=h;if(n===null)e.validator||x(de());else{const{value:l}=U;y({offset:l,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})}}function ne(){const{value:o}=ee;if(!o){Se();return}const{value:n}=h;if(n===null)e.validator||x(de());else{const{value:l}=U;y({offset:-l,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})}}const be=me,he=pe;function de(){if(e.validator)return null;const{value:o}=c,{value:n}=t;return o!==null?Math.max(0,o):n!==null?Math.min(0,n):0}function xe(o){ge(o),x(null)}function ye(o){var n,l,b;!((n=F.value)===null||n===void 0)&&n.$el.contains(o.target)&&o.preventDefault(),!((l=_.value)===null||l===void 0)&&l.$el.contains(o.target)&&o.preventDefault(),(b=s.value)===null||b===void 0||b.activate()}let H=null,L=null,ue=null;function Se(){ue&&(window.clearTimeout(ue),ue=null),H&&(window.clearInterval(H),H=null)}let ce=null;function Ce(){ce&&(window.clearTimeout(ce),ce=null),L&&(window.clearInterval(L),L=null)}function je(){Se(),ue=window.setTimeout(()=>{H=window.setInterval(()=>{ne()},Ue)},$e),ke("mouseup",document,Se,{once:!0})}function He(){Ce(),ce=window.setTimeout(()=>{L=window.setInterval(()=>{te()},Ue)},$e),ke("mouseup",document,Ce,{once:!0})}const Le=()=>{L||te()},Je=()=>{H||ne()};function Ke(o){var n,l;if(o.key==="Enter"){if(o.target===((n=s.value)===null||n===void 0?void 0:n.wrapperElRef))return;y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&((l=s.value)===null||l===void 0||l.deactivate())}else if(o.key==="ArrowUp"){if(!oe.value||e.keyboard.ArrowUp===!1)return;o.preventDefault(),y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&te()}else if(o.key==="ArrowDown"){if(!ee.value||e.keyboard.ArrowDown===!1)return;o.preventDefault(),y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&ne()}}function We(o){k.value=o,e.updateValueOnInput&&!e.format&&!e.parse&&e.precision===void 0&&y({offset:0,doUpdateIfValid:!0,isInputing:!0,fixPrecision:!1})}io(h,()=>{r()});const Ge={focus:()=>{var o;return(o=s.value)===null||o===void 0?void 0:o.focus()},blur:()=>{var o;return(o=s.value)===null||o===void 0?void 0:o.blur()},select:()=>{var o;return(o=s.value)===null||o===void 0?void 0:o.select()}},Xe=Ae("InputNumber",a,w);return Object.assign(Object.assign({},Ge),{rtlEnabled:Xe,inputInstRef:s,minusButtonInstRef:_,addButtonInstRef:F,mergedClsPrefix:w,mergedBordered:v,uncontrolledValue:$,mergedValue:h,mergedPlaceholder:Y,displayedValueInvalid:Z,mergedSize:I,mergedDisabled:C,displayedValue:k,addable:oe,minusable:ee,mergedStatus:i,handleFocus:be,handleBlur:he,handleClear:xe,handleMouseDown:ye,handleAddClick:Le,handleMinusClick:Je,handleAddMousedown:He,handleMinusMousedown:je,handleKeyDown:Ke,handleUpdateDisplayedValue:We,mergedTheme:g,inputThemeOverrides:{paddingSmall:"0 8px 0 10px",paddingMedium:"0 8px 0 12px",paddingLarge:"0 8px 0 14px"},buttonThemeOverrides:T(()=>{const{self:{iconColorDisabled:o}}=g.value,[n,l,b,N]=uo(o);return{textColorTextDisabled:`rgb(${n}, ${l}, ${b})`,opacityDisabled:`${N}`}})})},render(){const{mergedClsPrefix:e,$slots:v}=this,w=()=>p(Pe,{text:!0,disabled:!this.minusable||this.mergedDisabled||this.readonly,focusable:!1,theme:this.mergedTheme.peers.Button,themeOverrides:this.mergedTheme.peerOverrides.Button,builtinThemeOverrides:this.buttonThemeOverrides,onClick:this.handleMinusClick,onMousedown:this.handleMinusMousedown,ref:"minusButtonInstRef"},{icon:()=>Ne(v["minus-icon"],()=>[p(Oe,{clsPrefix:e},{default:()=>p(No,null)})])}),a=()=>p(Pe,{text:!0,disabled:!this.addable||this.mergedDisabled||this.readonly,focusable:!1,theme:this.mergedTheme.peers.Button,themeOverrides:this.mergedTheme.peerOverrides.Button,builtinThemeOverrides:this.buttonThemeOverrides,onClick:this.handleAddClick,onMousedown:this.handleAddMousedown,ref:"addButtonInstRef"},{icon:()=>Ne(v["add-icon"],()=>[p(Oe,{clsPrefix:e},{default:()=>p(Bo,null)})])});return p("div",{class:[`${e}-input-number`,this.rtlEnabled&&`${e}-input-number--rtl`]},p(Q,{ref:"inputInstRef",autofocus:this.autofocus,status:this.mergedStatus,bordered:this.mergedBordered,loading:this.loading,value:this.displayedValue,onUpdateValue:this.handleUpdateDisplayedValue,theme:this.mergedTheme.peers.Input,themeOverrides:this.mergedTheme.peerOverrides.Input,builtinThemeOverrides:this.inputThemeOverrides,size:this.mergedSize,placeholder:this.mergedPlaceholder,disabled:this.mergedDisabled,readonly:this.readonly,round:this.round,textDecoration:this.displayedValueInvalid?"line-through":void 0,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeydown:this.handleKeyDown,onMousedown:this.handleMouseDown,onClear:this.handleClear,clearable:this.clearable,inputProps:this.inputProps,internalLoadingBeforeSuffix:!0},{prefix:()=>{var m;return this.showButton&&this.buttonPlacement==="both"?[w(),D(v.prefix,g=>g?p("span",{class:`${e}-input-number-prefix`},g):null)]:(m=v.prefix)===null||m===void 0?void 0:m.call(v)},suffix:()=>{var m;return this.showButton?[D(v.suffix,g=>g?p("span",{class:`${e}-input-number-suffix`},g):null),this.buttonPlacement==="right"?w():null,a()]:(m=v.suffix)===null||m===void 0?void 0:m.call(v)}}))}}),Ho={class:"settings-view"},Lo={key:0,class:"settings-main"},Jo={key:1,class:"settings-main"},Ko={class:"provider-form"},Wo={class:"field"},Go={class:"field"},Xo={class:"field"},Qo={class:"field"},qo={class:"section-label"},Yo={class:"field"},Zo={class:"field"},et={class:"field"},ot={class:"provider-form",style:{"margin-top":"12px"}},tt={class:"field"},nt={class:"provider-form"},rt={class:"field"},lt={class:"field"},at={class:"inline"},it={class:"field-inline"},st={class:"actions"},dt=se({__name:"SettingsView",setup(e){const v=go(),w=_o(),a=A(!0),m=A(!1),g=A(null),u=bo({});let B="";fo(async()=>{try{const[c,t]=await Promise.all([vo(),mo()]);Object.assign(u,JSON.parse(JSON.stringify(c))),B=JSON.stringify(u),g.value=t}catch{w.error("加载配置失败")}finally{a.value=!1}});const I=T(()=>{const c={...u};delete c.available_devices;const t=JSON.parse(B||"{}");return delete t.available_devices,JSON.stringify(c)!==JSON.stringify(t)});function C(c){return T({get:()=>{var t,r;return((r=(((t=u.tts_provider)==null?void 0:t.providers)||[]).find(x=>x.name===c))==null?void 0:r.voice)||""},set:t=>{var y;const x=(((y=u.tts_provider)==null?void 0:y.providers)||[]).find(Z=>Z.name===c);x&&(x.voice=t)}})}const i=C("edge_tts"),s=C("cosyvoice"),_=C("sambert"),F=T(()=>{var c,t;return(((t=(c=g.value)==null?void 0:c.voices)==null?void 0:t.edge_tts)||[]).map(r=>({label:r,value:r}))}),$=T(()=>{var c,t;return(((t=(c=g.value)==null?void 0:c.voices)==null?void 0:t.cosyvoice)||[]).map(r=>({label:r,value:r}))}),j=T(()=>{var c,t;return(((t=(c=g.value)==null?void 0:c.voices)==null?void 0:t.sambert)||[]).map(r=>({label:r,value:r}))}),h=T(()=>{var c;return((c=u.translation_provider)==null?void 0:c.providers)||[]}),k=T(()=>(u.available_devices||[]).map(t=>({label:t.name,value:t.name}))),R=[{label:"中文",value:"中文"},{label:"英语",value:"英语"},{label:"日语",value:"日语"}];async function q(){m.value=!0;try{const c=JSON.parse(JSON.stringify(u));delete c.available_devices,await Co(c),B=JSON.stringify(u),w.success("已保存")}catch{w.error("保存失败")}finally{m.value=!1}}function Y(){Object.assign(u,JSON.parse(B)),w.info("已恢复")}const U=v.beforeEach((c,t,r)=>{t.name==="settings"&&I.value?window.confirm("有未保存的更改，是否放弃？")?r():r(!1):r()});return po(U),(c,t)=>(ae(),le("div",Ho,[a.value?(ae(),le("div",Lo,[...t[9]||(t[9]=[d("p",{class:"muted"},"加载中...",-1)])])):(ae(),le("div",Jo,[V(S(fe),{title:"TTS 引擎",size:"small"},{default:X(()=>[d("div",Ko,[d("label",Wo,[t[10]||(t[10]=d("span",null,"Edge TTS 音色",-1)),V(S(ie),{value:S(i),"onUpdate:value":t[0]||(t[0]=r=>Ie(i)?i.value=r:null),options:F.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",Go,[t[11]||(t[11]=d("span",null,"CosyVoice 音色",-1)),V(S(ie),{value:S(s),"onUpdate:value":t[1]||(t[1]=r=>Ie(s)?s.value=r:null),options:$.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",Xo,[t[12]||(t[12]=d("span",null,"Sambert 音色",-1)),V(S(ie),{value:S(_),"onUpdate:value":t[2]||(t[2]=r=>Ie(_)?_.value=r:null),options:j.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",Qo,[t[13]||(t[13]=d("span",null,"阿里 API Key",-1)),V(S(Q),{value:u.ali_api_key,"onUpdate:value":t[3]||(t[3]=r=>u.ali_api_key=r),type:"password","show-password-on":"click",size:"small"},null,8,["value"])])])]),_:1}),V(S(fe),{title:"翻译引擎",size:"small"},{default:X(()=>[(ae(!0),le(ho,null,xo(h.value,(r,x)=>(ae(),le("div",{key:x,class:"provider-form",style:yo({marginTop:x>0?"16px":"0"})},[d("div",qo,So(r.name),1),d("label",Yo,[t[14]||(t[14]=d("span",null,"API Key",-1)),V(S(Q),{value:h.value[x].api_key,"onUpdate:value":y=>h.value[x].api_key=y,type:"password","show-password-on":"click",size:"small"},null,8,["value","onUpdate:value"])]),d("label",Zo,[t[15]||(t[15]=d("span",null,"API URL",-1)),V(S(Q),{value:h.value[x].url,"onUpdate:value":y=>h.value[x].url=y,size:"small"},null,8,["value","onUpdate:value"])]),d("label",et,[t[16]||(t[16]=d("span",null,"Model",-1)),V(S(Q),{value:h.value[x].model,"onUpdate:value":y=>h.value[x].model=y,size:"small"},null,8,["value","onUpdate:value"])])],4))),128)),d("div",ot,[d("label",tt,[t[17]||(t[17]=d("span",null,"目标翻译语言",-1)),V(S(ie),{value:u.tLanguage,"onUpdate:value":t[4]||(t[4]=r=>u.tLanguage=r),options:R,size:"small",style:{width:"100%"}},null,8,["value"])])])]),_:1}),V(S(fe),{title:"语音识别",size:"small"},{default:X(()=>[...t[18]||(t[18]=[d("div",{class:"placeholder"},[d("span",{class:"placeholder-icon"},"⏳"),d("p",null,"Phase 2 开放")],-1)])]),_:1}),V(S(fe),{title:"音频 & OSC",size:"small"},{default:X(()=>[d("div",nt,[d("label",rt,[t[19]||(t[19]=d("span",null,"播放设备",-1)),V(S(ie),{value:u.device,"onUpdate:value":t[5]||(t[5]=r=>u.device=r),options:k.value,filterable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",lt,[t[21]||(t[21]=d("span",null,"OSC 地址",-1)),d("div",at,[V(S(Q),{value:u.osc_host,"onUpdate:value":t[6]||(t[6]=r=>u.osc_host=r),size:"small",style:{width:"140px"}},null,8,["value"]),t[20]||(t[20]=d("span",{class:"sep"},":",-1)),V(S(jo),{value:u.osc_port,"onUpdate:value":t[7]||(t[7]=r=>u.osc_port=r),min:1,max:65535,size:"small",style:{width:"100px"}},null,8,["value"])])]),d("label",it,[t[22]||(t[22]=d("span",null,"OSC 启用",-1)),V(S(Io),{value:u.osc_enabled,"onUpdate:value":t[8]||(t[8]=r=>u.osc_enabled=r),size:"small"},null,8,["value"])])])]),_:1}),d("div",st,[V(S(Me),{onClick:Y,disabled:!I.value},{default:X(()=>[...t[23]||(t[23]=[Re("取消",-1)])]),_:1},8,["disabled"]),V(S(Me),{type:"primary",onClick:q,loading:m.value,disabled:!I.value},{default:X(()=>[...t[24]||(t[24]=[Re(" 保存 ",-1)])]),_:1},8,["loading","disabled"])])]))]))}}),mt=wo(dt,[["__scopeId","data-v-a9dd5012"]]);export{mt as default};
