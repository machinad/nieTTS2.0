import{C as ie,L as p,E as Ee,i as f,j as z,h as Qe,l as M,k,P as Xe,Q as Ye,ac as A,ak as Ae,as as ve,aq as De,at as Ze,G as W,S as eo,a as oo,n as K,s as T,y as Ie,K as to,af as no,O as ro,U as lo,A as ao,am as so,al as io,a8 as D,ao as uo,an as J,au as co,aa as Ne,b as ke,W as fo,$ as Re,ad as vo,ah as mo,a1 as po,H as go,I as bo,a0 as ho,w as le,u as d,B as I,aw as q,aj as S,ap as xo,a7 as yo,a2 as ae,g as se,R as Ve,F as So,a9 as wo,Y as Co,ag as zo,z as Oe,a3 as Io,_ as Vo}from"./index-CEMDB6DU.js";import{i as _o,b as Bo,N as Q,X as Pe,B as Me,a as No}from"./Switch-UKPxvuES.js";const ko=ie({name:"Add",render(){return p("svg",{width:"512",height:"512",viewBox:"0 0 512 512",fill:"none",xmlns:"http://www.w3.org/2000/svg"},p("path",{d:"M256 112V400M400 256H112",stroke:"currentColor","stroke-width":"32","stroke-linecap":"round","stroke-linejoin":"round"}))}}),Ro=ie({name:"Remove",render(){return p("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 512 512"},p("line",{x1:"400",y1:"256",x2:"112",y2:"256",style:`
        fill: none;
        stroke: currentColor;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-width: 32px;
      `}))}}),Oo={paddingSmall:"12px 16px 12px",paddingMedium:"19px 24px 20px",paddingLarge:"23px 32px 24px",paddingHuge:"27px 40px 28px",titleFontSizeSmall:"16px",titleFontSizeMedium:"18px",titleFontSizeLarge:"18px",titleFontSizeHuge:"18px",closeIconSize:"18px",closeSize:"22px"};function Po(e){const{primaryColor:v,borderRadius:C,lineHeight:a,fontSize:m,cardColor:g,textColor2:u,textColor1:B,dividerColor:V,fontWeightStrong:w,closeIconColor:s,closeIconColorHover:i,closeIconColorPressed:_,closeColorHover:F,closeColorPressed:$,modalColor:j,boxShadow1:h,popoverColor:R,actionColor:O}=e;return Object.assign(Object.assign({},Oo),{lineHeight:a,color:g,colorModal:j,colorPopover:R,colorTarget:v,colorEmbedded:O,colorEmbeddedModal:O,colorEmbeddedPopover:O,textColor:u,titleTextColor:B,borderColor:V,actionColor:O,titleFontWeight:w,closeColorHover:F,closeColorPressed:$,closeBorderRadius:C,closeIconColor:s,closeIconColorHover:i,closeIconColorPressed:_,fontSizeSmall:m,fontSizeMedium:m,fontSizeLarge:m,fontSizeHuge:m,boxShadow:h,borderRadius:C})}const Mo={common:Ee,self:Po},Fe=z("card-content",`
 flex: 1;
 min-width: 0;
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
`),Fo=f([z("card",`
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
 `),k("content-scrollbar",[f(">",[z("scrollbar-container",[f(">",[z("card-content",`
 padding-top: var(--n-padding-bottom);
 `)])])])])])]),M("content-soft-segmented",[f(">",[z("card-content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `),k("content-scrollbar",[f(">",[z("scrollbar-container",[f(">",[z("card-content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `)])])])])])]),M("footer-segmented",[f(">",[k("footer",`
 padding-top: var(--n-padding-bottom);
 `)])]),M("footer-soft-segmented",[f(">",[k("footer",`
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
 `,[k("main",`
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 flex: 1;
 min-width: 0;
 color: var(--n-title-text-color);
 `),k("extra",`
 display: flex;
 align-items: center;
 font-size: var(--n-font-size);
 font-weight: 400;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 `),k("close",`
 margin: 0 0 0 8px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `)]),k("action",`
 box-sizing: border-box;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 background-clip: padding-box;
 background-color: var(--n-action-color);
 `),Fe,z("card-content",[f("&:first-child",`
 padding-top: var(--n-padding-bottom);
 `)]),k("content-scrollbar",`
 display: flex;
 flex-direction: column;
 `,[f(">",[z("scrollbar-container",[f(">",[Fe])])]),f("&:first-child >",[z("scrollbar-container",[f(">",[z("card-content",`
 padding-top: var(--n-padding-bottom);
 `)])])])]),k("footer",`
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
 `,[f("&:first-child",`
 padding-top: var(--n-padding-bottom);
 `)]),k("action",`
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
 `,[f("&:target","border-color: var(--n-color-target);")]),M("action-segmented",[f(">",[k("action",[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),M("content-segmented, content-soft-segmented",[f(">",[z("card-content",`
 transition: border-color 0.3s var(--n-bezier);
 `,[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)]),k("content-scrollbar",`
 transition: border-color 0.3s var(--n-bezier);
 `,[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),M("footer-segmented, footer-soft-segmented",[f(">",[k("footer",`
 transition: border-color 0.3s var(--n-bezier);
 `,[f("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),M("embedded",`
 background-color: var(--n-color-embedded);
 `)]),Xe(z("card",`
 background: var(--n-color-modal);
 `,[M("embedded",`
 background-color: var(--n-color-embedded-modal);
 `)])),Ye(z("card",`
 background: var(--n-color-popover);
 `,[M("embedded",`
 background-color: var(--n-color-embedded-popover);
 `)]))]),To={title:[String,Function],contentClass:String,contentStyle:[Object,String],contentScrollable:Boolean,headerClass:String,headerStyle:[Object,String],headerExtraClass:String,headerExtraStyle:[Object,String],footerClass:String,footerStyle:[Object,String],embedded:Boolean,segmented:{type:[Boolean,Object],default:!1},size:String,bordered:{type:Boolean,default:!0},closable:Boolean,hoverable:Boolean,role:String,onClose:[Function,Array],tag:{type:String,default:"div"},cover:Function,content:[String,Function],footer:Function,action:Function,headerExtra:Function,closeFocusable:Boolean},$o=Object.assign(Object.assign({},ve.props),To),fe=ie({name:"Card",props:$o,slots:Object,setup(e){const v=()=>{const{onClose:i}=e;i&&K(i)},{inlineThemeDisabled:C,mergedClsPrefixRef:a,mergedRtlRef:m,mergedComponentPropsRef:g}=Ae(e),u=ve("Card","-card",Fo,Mo,e,a),B=De("Card",m,a),V=T(()=>{var i,_;return e.size||((_=(i=g==null?void 0:g.value)===null||i===void 0?void 0:i.Card)===null||_===void 0?void 0:_.size)||"medium"}),w=T(()=>{const i=V.value,{self:{color:_,colorModal:F,colorTarget:$,textColor:j,titleTextColor:h,titleFontWeight:R,borderColor:O,actionColor:X,borderRadius:Y,lineHeight:U,closeIconColor:c,closeIconColorHover:t,closeIconColorPressed:r,closeColorHover:x,closeColorPressed:y,closeBorderRadius:Z,closeIconSize:ee,closeSize:oe,boxShadow:me,colorPopover:pe,colorEmbedded:ge,colorEmbeddedModal:te,colorEmbeddedPopover:ne,[Ie("padding",i)]:be,[Ie("fontSize",i)]:he,[Ie("titleFontSize",i)]:de},common:{cubicBezierEaseInOut:xe}}=u.value,{top:ye,left:H,bottom:L}=to(be);return{"--n-bezier":xe,"--n-border-radius":Y,"--n-color":_,"--n-color-modal":F,"--n-color-popover":pe,"--n-color-embedded":ge,"--n-color-embedded-modal":te,"--n-color-embedded-popover":ne,"--n-color-target":$,"--n-text-color":j,"--n-line-height":U,"--n-action-color":X,"--n-title-text-color":h,"--n-title-font-weight":R,"--n-close-icon-color":c,"--n-close-icon-color-hover":t,"--n-close-icon-color-pressed":r,"--n-close-color-hover":x,"--n-close-color-pressed":y,"--n-border-color":O,"--n-box-shadow":me,"--n-padding-top":ye,"--n-padding-bottom":L,"--n-padding-left":H,"--n-font-size":he,"--n-title-font-size":de,"--n-close-size":oe,"--n-close-icon-size":ee,"--n-close-border-radius":Z}}),s=C?Ze("card",T(()=>V.value[0]),w,e):void 0;return{rtlEnabled:B,mergedClsPrefix:a,mergedTheme:u,handleCloseClick:v,cssVars:C?void 0:w,themeClass:s==null?void 0:s.themeClass,onRender:s==null?void 0:s.onRender}},render(){const{segmented:e,bordered:v,hoverable:C,mergedClsPrefix:a,rtlEnabled:m,onRender:g,embedded:u,tag:B,$slots:V}=this;return g==null||g(),p(B,{class:[`${a}-card`,this.themeClass,u&&`${a}-card--embedded`,{[`${a}-card--rtl`]:m,[`${a}-card--content-scrollable`]:this.contentScrollable,[`${a}-card--content${typeof e!="boolean"&&e.content==="soft"?"-soft":""}-segmented`]:e===!0||e!==!1&&e.content,[`${a}-card--footer${typeof e!="boolean"&&e.footer==="soft"?"-soft":""}-segmented`]:e===!0||e!==!1&&e.footer,[`${a}-card--action-segmented`]:e===!0||e!==!1&&e.action,[`${a}-card--bordered`]:v,[`${a}-card--hoverable`]:C}],style:this.cssVars,role:this.role},A(V.cover,w=>{const s=this.cover?W([this.cover()]):w;return s&&p("div",{class:`${a}-card-cover`,role:"none"},s)}),A(V.header,w=>{const{title:s}=this,i=s?W(typeof s=="function"?[s()]:[s]):w;return i||this.closable?p("div",{class:[`${a}-card-header`,this.headerClass],style:this.headerStyle,role:"heading"},p("div",{class:`${a}-card-header__main`,role:"heading"},i),A(V["header-extra"],_=>{const F=this.headerExtra?W([this.headerExtra()]):_;return F&&p("div",{class:[`${a}-card-header__extra`,this.headerExtraClass],style:this.headerExtraStyle},F)}),this.closable&&p(oo,{clsPrefix:a,class:`${a}-card-header__close`,onClick:this.handleCloseClick,focusable:this.closeFocusable,absolute:!0})):null}),A(V.default,w=>{const{content:s}=this,i=s?W(typeof s=="function"?[s()]:[s]):w;return i?this.contentScrollable?p(eo,{class:`${a}-card__content-scrollbar`,contentClass:[`${a}-card-content`,this.contentClass],contentStyle:this.contentStyle},i):p("div",{class:[`${a}-card-content`,this.contentClass],style:this.contentStyle,role:"none"},i):null}),A(V.footer,w=>{const s=this.footer?W([this.footer()]):w;return s&&p("div",{class:[`${a}-card__footer`,this.footerClass],style:this.footerStyle,role:"none"},s)}),A(V.action,w=>{const s=this.action?W([this.action()]):w;return s&&p("div",{class:`${a}-card__action`,role:"none"},s)}))}});function Uo(){const e=ro(lo,null);return e===null&&no("use-message","No outer <n-message-provider /> founded. See prerequisite in https://www.naiveui.com/en-US/os-theme/components/message for more details. If you want to use `useMessage` outside setup, please check https://www.naiveui.com/zh-CN/os-theme/components/message#Q-&-A."),e}function Eo(e){const{textColorDisabled:v}=e;return{iconColorDisabled:v}}const Ao=ao({name:"InputNumber",common:Ee,peers:{Button:Bo,Input:_o},self:Eo}),Do=f([z("input-number-suffix",`
 display: inline-block;
 margin-right: 10px;
 `),z("input-number-prefix",`
 display: inline-block;
 margin-left: 10px;
 `)]);function jo(e){return e==null||typeof e=="string"&&e.trim()===""?null:Number(e)}function Ho(e){return e.includes(".")&&(/^(-)?\d+.*(\.|0)$/.test(e)||/^-?\d*$/.test(e))||e==="-"||e==="-0"}function _e(e){return e==null?!0:!Number.isNaN(e)}function Te(e,v){return typeof e!="number"?"":v===void 0?String(e):e.toFixed(v)}function Be(e){if(e===null)return null;if(typeof e=="number")return e;{const v=Number(e);return Number.isNaN(v)?null:v}}const $e=800,Ue=100,Lo=Object.assign(Object.assign({},ve.props),{autofocus:Boolean,loading:{type:Boolean,default:void 0},placeholder:String,defaultValue:{type:Number,default:null},value:Number,step:{type:[Number,String],default:1},min:[Number,String],max:[Number,String],size:String,disabled:{type:Boolean,default:void 0},validator:Function,bordered:{type:Boolean,default:void 0},showButton:{type:Boolean,default:!0},buttonPlacement:{type:String,default:"right"},inputProps:Object,readonly:Boolean,clearable:Boolean,keyboard:{type:Object,default:{}},updateValueOnInput:{type:Boolean,default:!0},round:{type:Boolean,default:void 0},parse:Function,format:Function,precision:Number,status:String,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onFocus:[Function,Array],onBlur:[Function,Array],onClear:[Function,Array],onChange:[Function,Array]}),Jo=ie({name:"InputNumber",props:Lo,slots:Object,setup(e){const{mergedBorderedRef:v,mergedClsPrefixRef:C,mergedRtlRef:a,mergedComponentPropsRef:m}=Ae(e),g=ve("InputNumber","-input-number",Do,Ao,e,C),{localeRef:u}=so("InputNumber"),B=io(e,{mergedSize:o=>{var n,l;const{size:b}=e;if(b)return b;const{mergedSize:N}=o||{};if(N!=null&&N.value)return N.value;const P=(l=(n=m==null?void 0:m.value)===null||n===void 0?void 0:n.InputNumber)===null||l===void 0?void 0:l.size;return P||"medium"}}),{mergedSizeRef:V,mergedDisabledRef:w,mergedStatusRef:s}=B,i=D(null),_=D(null),F=D(null),$=D(e.defaultValue),j=mo(e,"value"),h=uo(j,$),R=D(""),O=o=>{const n=String(o).split(".")[1];return n?n.length:0},X=o=>{const n=[e.min,e.max,e.step,o].map(l=>l===void 0?0:O(l));return Math.max(...n)},Y=J(()=>{const{placeholder:o}=e;return o!==void 0?o:u.value.placeholder}),U=J(()=>{const o=Be(e.step);return o!==null?o===0?1:Math.abs(o):1}),c=J(()=>{const o=Be(e.min);return o!==null?o:null}),t=J(()=>{const o=Be(e.max);return o!==null?o:null}),r=()=>{const{value:o}=h;if(_e(o)){const{format:n,precision:l}=e;n?R.value=n(o):o===null||l===void 0||O(o)>l?R.value=Te(o,void 0):R.value=Te(o,l)}else R.value=String(o)};r();const x=o=>{const{value:n}=h;if(o===n){r();return}const{"onUpdate:value":l,onUpdateValue:b,onChange:N}=e,{nTriggerFormInput:P,nTriggerFormChange:G}=B;N&&K(N,o),b&&K(b,o),l&&K(l,o),$.value=o,P(),G()},y=({offset:o,doUpdateIfValid:n,fixPrecision:l,isInputing:b})=>{const{value:N}=R;if(b&&Ho(N))return!1;const P=(e.parse||jo)(N);if(P===null)return n&&x(null),null;if(_e(P)){const G=O(P),{precision:re}=e;if(re!==void 0&&re<G&&!l)return!1;let E=Number.parseFloat((P+o).toFixed(re??X(P)));if(_e(E)){const{value:Ce}=t,{value:ze}=c;if(Ce!==null&&E>Ce){if(!n||b)return!1;E=Ce}if(ze!==null&&E<ze){if(!n||b)return!1;E=ze}return e.validator&&!e.validator(E)?!1:(n&&x(E),E)}}return!1},Z=J(()=>y({offset:0,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})===!1),ee=J(()=>{const{value:o}=h;if(e.validator&&o===null)return!1;const{value:n}=U;return y({offset:-n,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})!==!1}),oe=J(()=>{const{value:o}=h;if(e.validator&&o===null)return!1;const{value:n}=U;return y({offset:+n,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})!==!1});function me(o){const{onFocus:n}=e,{nTriggerFormFocus:l}=B;n&&K(n,o),l()}function pe(o){var n,l;if(o.target===((n=i.value)===null||n===void 0?void 0:n.wrapperElRef))return;const b=y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0});if(b!==!1){const G=(l=i.value)===null||l===void 0?void 0:l.inputElRef;G&&(G.value=String(b||"")),h.value===b&&r()}else r();const{onBlur:N}=e,{nTriggerFormBlur:P}=B;N&&K(N,o),P(),fo(()=>{r()})}function ge(o){const{onClear:n}=e;n&&K(n,o)}function te(){const{value:o}=oe;if(!o){we();return}const{value:n}=h;if(n===null)e.validator||x(de());else{const{value:l}=U;y({offset:l,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})}}function ne(){const{value:o}=ee;if(!o){Se();return}const{value:n}=h;if(n===null)e.validator||x(de());else{const{value:l}=U;y({offset:-l,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})}}const be=me,he=pe;function de(){if(e.validator)return null;const{value:o}=c,{value:n}=t;return o!==null?Math.max(0,o):n!==null?Math.min(0,n):0}function xe(o){ge(o),x(null)}function ye(o){var n,l,b;!((n=F.value)===null||n===void 0)&&n.$el.contains(o.target)&&o.preventDefault(),!((l=_.value)===null||l===void 0)&&l.$el.contains(o.target)&&o.preventDefault(),(b=i.value)===null||b===void 0||b.activate()}let H=null,L=null,ue=null;function Se(){ue&&(window.clearTimeout(ue),ue=null),H&&(window.clearInterval(H),H=null)}let ce=null;function we(){ce&&(window.clearTimeout(ce),ce=null),L&&(window.clearInterval(L),L=null)}function je(){Se(),ue=window.setTimeout(()=>{H=window.setInterval(()=>{ne()},Ue)},$e),Re("mouseup",document,Se,{once:!0})}function He(){we(),ce=window.setTimeout(()=>{L=window.setInterval(()=>{te()},Ue)},$e),Re("mouseup",document,we,{once:!0})}const Le=()=>{L||te()},Je=()=>{H||ne()};function Ke(o){var n,l;if(o.key==="Enter"){if(o.target===((n=i.value)===null||n===void 0?void 0:n.wrapperElRef))return;y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&((l=i.value)===null||l===void 0||l.deactivate())}else if(o.key==="ArrowUp"){if(!oe.value||e.keyboard.ArrowUp===!1)return;o.preventDefault(),y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&te()}else if(o.key==="ArrowDown"){if(!ee.value||e.keyboard.ArrowDown===!1)return;o.preventDefault(),y({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&ne()}}function Ge(o){R.value=o,e.updateValueOnInput&&!e.format&&!e.parse&&e.precision===void 0&&y({offset:0,doUpdateIfValid:!0,isInputing:!0,fixPrecision:!1})}co(h,()=>{r()});const We={focus:()=>{var o;return(o=i.value)===null||o===void 0?void 0:o.focus()},blur:()=>{var o;return(o=i.value)===null||o===void 0?void 0:o.blur()},select:()=>{var o;return(o=i.value)===null||o===void 0?void 0:o.select()}},qe=De("InputNumber",a,C);return Object.assign(Object.assign({},We),{rtlEnabled:qe,inputInstRef:i,minusButtonInstRef:_,addButtonInstRef:F,mergedClsPrefix:C,mergedBordered:v,uncontrolledValue:$,mergedValue:h,mergedPlaceholder:Y,displayedValueInvalid:Z,mergedSize:V,mergedDisabled:w,displayedValue:R,addable:oe,minusable:ee,mergedStatus:s,handleFocus:be,handleBlur:he,handleClear:xe,handleMouseDown:ye,handleAddClick:Le,handleMinusClick:Je,handleAddMousedown:He,handleMinusMousedown:je,handleKeyDown:Ke,handleUpdateDisplayedValue:Ge,mergedTheme:g,inputThemeOverrides:{paddingSmall:"0 8px 0 10px",paddingMedium:"0 8px 0 12px",paddingLarge:"0 8px 0 14px"},buttonThemeOverrides:T(()=>{const{self:{iconColorDisabled:o}}=g.value,[n,l,b,N]=vo(o);return{textColorTextDisabled:`rgb(${n}, ${l}, ${b})`,opacityDisabled:`${N}`}})})},render(){const{mergedClsPrefix:e,$slots:v}=this,C=()=>p(Pe,{text:!0,disabled:!this.minusable||this.mergedDisabled||this.readonly,focusable:!1,theme:this.mergedTheme.peers.Button,themeOverrides:this.mergedTheme.peerOverrides.Button,builtinThemeOverrides:this.buttonThemeOverrides,onClick:this.handleMinusClick,onMousedown:this.handleMinusMousedown,ref:"minusButtonInstRef"},{icon:()=>Ne(v["minus-icon"],()=>[p(ke,{clsPrefix:e},{default:()=>p(Ro,null)})])}),a=()=>p(Pe,{text:!0,disabled:!this.addable||this.mergedDisabled||this.readonly,focusable:!1,theme:this.mergedTheme.peers.Button,themeOverrides:this.mergedTheme.peerOverrides.Button,builtinThemeOverrides:this.buttonThemeOverrides,onClick:this.handleAddClick,onMousedown:this.handleAddMousedown,ref:"addButtonInstRef"},{icon:()=>Ne(v["add-icon"],()=>[p(ke,{clsPrefix:e},{default:()=>p(ko,null)})])});return p("div",{class:[`${e}-input-number`,this.rtlEnabled&&`${e}-input-number--rtl`]},p(Q,{ref:"inputInstRef",autofocus:this.autofocus,status:this.mergedStatus,bordered:this.mergedBordered,loading:this.loading,value:this.displayedValue,onUpdateValue:this.handleUpdateDisplayedValue,theme:this.mergedTheme.peers.Input,themeOverrides:this.mergedTheme.peerOverrides.Input,builtinThemeOverrides:this.inputThemeOverrides,size:this.mergedSize,placeholder:this.mergedPlaceholder,disabled:this.mergedDisabled,readonly:this.readonly,round:this.round,textDecoration:this.displayedValueInvalid?"line-through":void 0,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeydown:this.handleKeyDown,onMousedown:this.handleMouseDown,onClear:this.handleClear,clearable:this.clearable,inputProps:this.inputProps,internalLoadingBeforeSuffix:!0},{prefix:()=>{var m;return this.showButton&&this.buttonPlacement==="both"?[C(),A(v.prefix,g=>g?p("span",{class:`${e}-input-number-prefix`},g):null)]:(m=v.prefix)===null||m===void 0?void 0:m.call(v)},suffix:()=>{var m;return this.showButton?[A(v.suffix,g=>g?p("span",{class:`${e}-input-number-suffix`},g):null),this.buttonPlacement==="right"?C():null,a()]:(m=v.suffix)===null||m===void 0?void 0:m.call(v)}}))}}),Ko={class:"settings-view"},Go={key:0,class:"settings-main"},Wo={key:1,class:"settings-main"},qo={class:"provider-form"},Qo={class:"field"},Xo={class:"field"},Yo={class:"field"},Zo={class:"field"},et={class:"section-label"},ot={class:"field"},tt={class:"field"},nt={class:"field"},rt={class:"provider-form",style:{"margin-top":"12px"}},lt={class:"field"},at={class:"provider-form"},st={class:"field"},it={class:"field"},dt={class:"inline"},ut={class:"field-inline"},ct={class:"actions"},ft=ie({__name:"SettingsView",setup(e){const v=xo(),C=Uo(),a=D(!0),m=D(!1),g=D(null),u=yo({});let B="";po(async()=>{try{const[c,t]=await Promise.all([go(),bo()]);Object.assign(u,JSON.parse(JSON.stringify(c))),B=JSON.stringify(u),g.value=t}catch{C.error("加载配置失败")}finally{a.value=!1}});const V=T(()=>JSON.stringify(u)!==B);function w(c){return T({get:()=>{var t,r;return((r=(((t=u.tts_provider)==null?void 0:t.providers)||[]).find(x=>x.name===c))==null?void 0:r.voice)||""},set:t=>{var y;const x=(((y=u.tts_provider)==null?void 0:y.providers)||[]).find(Z=>Z.name===c);x&&(x.voice=t)}})}const s=w("edge_tts"),i=w("cosyvoice"),_=w("sambert"),F=T(()=>{var c,t;return(((t=(c=g.value)==null?void 0:c.voices)==null?void 0:t.edge_tts)||[]).map(r=>({label:r,value:r}))}),$=T(()=>{var c,t;return(((t=(c=g.value)==null?void 0:c.voices)==null?void 0:t.cosyvoice)||[]).map(r=>({label:r,value:r}))}),j=T(()=>{var c,t;return(((t=(c=g.value)==null?void 0:c.voices)==null?void 0:t.sambert)||[]).map(r=>({label:r,value:r}))}),h=T(()=>{var c;return((c=u.translation_provider)==null?void 0:c.providers)||[]}),R=T(()=>(u.available_devices||[]).map(t=>({label:t.name,value:t.name}))),O=[{label:"中文",value:"中文"},{label:"英语",value:"英语"},{label:"日语",value:"日语"}];async function X(){m.value=!0;try{const c=JSON.parse(JSON.stringify(u));delete c.available_devices,await Io(c),B=JSON.stringify(u),C.success("已保存")}catch{C.error("保存失败")}finally{m.value=!1}}function Y(){Object.assign(u,JSON.parse(B)),C.info("已恢复")}const U=v.beforeEach((c,t,r)=>{t.name==="settings"&&V.value?window.confirm("有未保存的更改，是否放弃？")?r():r(!1):r()});return ho(U),(c,t)=>(ae(),le("div",Ko,[a.value?(ae(),le("div",Go,[...t[9]||(t[9]=[d("p",{class:"muted"},"加载中...",-1)])])):(ae(),le("div",Wo,[I(S(fe),{title:"TTS 引擎",size:"small"},{default:q(()=>[d("div",qo,[d("label",Qo,[t[10]||(t[10]=d("span",null,"Edge TTS 音色",-1)),I(S(se),{value:S(s),"onUpdate:value":t[0]||(t[0]=r=>Ve(s)?s.value=r:null),options:F.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",Xo,[t[11]||(t[11]=d("span",null,"CosyVoice 音色",-1)),I(S(se),{value:S(i),"onUpdate:value":t[1]||(t[1]=r=>Ve(i)?i.value=r:null),options:$.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",Yo,[t[12]||(t[12]=d("span",null,"Sambert 音色",-1)),I(S(se),{value:S(_),"onUpdate:value":t[2]||(t[2]=r=>Ve(_)?_.value=r:null),options:j.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",Zo,[t[13]||(t[13]=d("span",null,"阿里 API Key",-1)),I(S(Q),{value:u.ali_api_key,"onUpdate:value":t[3]||(t[3]=r=>u.ali_api_key=r),type:"password","show-password-on":"click",size:"small"},null,8,["value"])])])]),_:1}),I(S(fe),{title:"翻译引擎",size:"small"},{default:q(()=>[(ae(!0),le(So,null,wo(h.value,(r,x)=>(ae(),le("div",{key:x,class:"provider-form",style:Co({marginTop:x>0?"16px":"0"})},[d("div",et,zo(r.name),1),d("label",ot,[t[14]||(t[14]=d("span",null,"API Key",-1)),I(S(Q),{value:h.value[x].api_key,"onUpdate:value":y=>h.value[x].api_key=y,type:"password","show-password-on":"click",size:"small"},null,8,["value","onUpdate:value"])]),d("label",tt,[t[15]||(t[15]=d("span",null,"API URL",-1)),I(S(Q),{value:h.value[x].url,"onUpdate:value":y=>h.value[x].url=y,size:"small"},null,8,["value","onUpdate:value"])]),d("label",nt,[t[16]||(t[16]=d("span",null,"Model",-1)),I(S(Q),{value:h.value[x].model,"onUpdate:value":y=>h.value[x].model=y,size:"small"},null,8,["value","onUpdate:value"])])],4))),128)),d("div",rt,[d("label",lt,[t[17]||(t[17]=d("span",null,"目标翻译语言",-1)),I(S(se),{value:u.tLanguage,"onUpdate:value":t[4]||(t[4]=r=>u.tLanguage=r),options:O,size:"small",style:{width:"100%"}},null,8,["value"])])])]),_:1}),I(S(fe),{title:"语音识别",size:"small"},{default:q(()=>[...t[18]||(t[18]=[d("div",{class:"placeholder"},[d("span",{class:"placeholder-icon"},"⏳"),d("p",null,"Phase 2 开放")],-1)])]),_:1}),I(S(fe),{title:"音频 & OSC",size:"small"},{default:q(()=>[d("div",at,[d("label",st,[t[19]||(t[19]=d("span",null,"播放设备",-1)),I(S(se),{value:u.device,"onUpdate:value":t[5]||(t[5]=r=>u.device=r),options:R.value,filterable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),d("label",it,[t[21]||(t[21]=d("span",null,"OSC 地址",-1)),d("div",dt,[I(S(Q),{value:u.osc_host,"onUpdate:value":t[6]||(t[6]=r=>u.osc_host=r),size:"small",style:{width:"140px"}},null,8,["value"]),t[20]||(t[20]=d("span",{class:"sep"},":",-1)),I(S(Jo),{value:u.osc_port,"onUpdate:value":t[7]||(t[7]=r=>u.osc_port=r),min:1,max:65535,size:"small",style:{width:"100px"}},null,8,["value"])])]),d("label",ut,[t[22]||(t[22]=d("span",null,"OSC 启用",-1)),I(S(No),{value:u.osc_enabled,"onUpdate:value":t[8]||(t[8]=r=>u.osc_enabled=r),size:"small"},null,8,["value"])])])]),_:1}),d("div",ct,[I(S(Me),{onClick:Y,disabled:!V.value},{default:q(()=>[...t[23]||(t[23]=[Oe("取消",-1)])]),_:1},8,["disabled"]),I(S(Me),{type:"primary",onClick:X,loading:m.value,disabled:!V.value},{default:q(()=>[...t[24]||(t[24]=[Oe(" 保存 ",-1)])]),_:1},8,["loading","disabled"])])]))]))}}),pt=Vo(ft,[["__scopeId","data-v-4a419e80"]]);export{pt as default};
