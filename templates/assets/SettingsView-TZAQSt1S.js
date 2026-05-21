import{H as be,R as f,G as Kt,ai as j,aE as Yt,i as et,a0 as qt,Z as Oe,ap as Qt,J as Qe,j as m,k as o,h as Zt,m as v,l as M,X as ea,Y as ta,an as ae,ax as Ze,aG as we,aD as ht,aH as xt,K as Ce,S as aa,a as yt,o as Z,u as G,B as K,Q as $e,ar as na,W as St,a2 as oa,D as ra,az as la,ay as ia,aB as Ct,aA as me,aJ as ke,al as tt,b as qe,a3 as Le,a8 as at,ao as sa,at as Q,A as da,a1 as ca,F as Me,aj as ua,a7 as ba,n as fa,O as De,V as Ue,ab as wt,aa as pa,aK as va,aw as nt,I as ga,aM as ma,T as ha,q as xa,aI as ya,af as Sa,L as Ca,M as wa,a9 as za,z as ce,w as y,E as W,aL as ue,av as V,aC as Ta,ah as Ra,ac as re,g as Be,ak as ot,x as Pa,y as rt,a5 as _a,as as Ba,C as lt,ad as $a,_ as Ia}from"./index-DGUqA-Ox.js";import{i as Va,b as ka,N as Y,X as it,B as st,a as La}from"./Switch-Rqk_CUib.js";const Ma=et(".v-x-scroll",{overflow:"auto",scrollbarWidth:"none"},[et("&::-webkit-scrollbar",{width:0,height:0})]),Oa=be({name:"XScroll",props:{disabled:Boolean,onScroll:Function},setup(){const e=j(null);function l(c){!(c.currentTarget.offsetWidth<c.currentTarget.scrollWidth)||c.deltaY===0||(c.currentTarget.scrollLeft+=c.deltaY+c.deltaX,c.preventDefault())}const s=Yt();return Ma.mount({id:"vueuc/x-scroll",head:!0,anchorMetaName:Kt,ssr:s}),Object.assign({selfRef:e,handleWheel:l},{scrollTo(...c){var C;(C=e.value)===null||C===void 0||C.scrollTo(...c)}})},render(){return f("div",{ref:"selfRef",onScroll:this.onScroll,onWheel:this.disabled?void 0:this.handleWheel,class:"v-x-scroll"},this.$slots)}});var Ea=/\s/;function Aa(e){for(var l=e.length;l--&&Ea.test(e.charAt(l)););return l}var Na=/^\s+/;function Fa(e){return e&&e.slice(0,Aa(e)+1).replace(Na,"")}var dt=NaN,Wa=/^[-+]0x[0-9a-f]+$/i,ja=/^0b[01]+$/i,Ha=/^0o[0-7]+$/i,Da=parseInt;function ct(e){if(typeof e=="number")return e;if(qt(e))return dt;if(Oe(e)){var l=typeof e.valueOf=="function"?e.valueOf():e;e=Oe(l)?l+"":l}if(typeof e!="string")return e===0?e:+e;e=Fa(e);var s=ja.test(e);return s||Ha.test(e)?Da(e.slice(2),s?2:8):Wa.test(e)?dt:+e}var Ge=function(){return Qt.Date.now()},Ua="Expected a function",Ga=Math.max,Ja=Math.min;function Xa(e,l,s){var d,c,C,h,i,w,z=0,p=!1,u=!1,L=!0;if(typeof e!="function")throw new TypeError(Ua);l=ct(l)||0,Oe(s)&&(p=!!s.leading,u="maxWait"in s,C=u?Ga(ct(s.maxWait)||0,l):C,L="trailing"in s?!!s.trailing:L);function I(x){var B=d,a=c;return d=c=void 0,z=x,h=e.apply(a,B),h}function _(x){return z=x,i=setTimeout(O,l),p?I(x):h}function F(x){var B=x-w,a=x-z,S=l-B;return u?Ja(S,C-a):S}function k(x){var B=x-w,a=x-z;return w===void 0||B>=l||B<0||u&&a>=C}function O(){var x=Ge();if(k(x))return E(x);i=setTimeout(O,F(x))}function E(x){return i=void 0,L&&d?I(x):(d=c=void 0,h)}function J(){i!==void 0&&clearTimeout(i),z=0,d=w=c=i=void 0}function H(){return i===void 0?h:E(Ge())}function $(){var x=Ge(),B=k(x);if(d=arguments,c=this,w=x,B){if(i===void 0)return _(w);if(u)return clearTimeout(i),i=setTimeout(O,l),I(w)}return i===void 0&&(i=setTimeout(O,l)),h}return $.cancel=J,$.flush=H,$}var Ka="Expected a function";function Ya(e,l,s){var d=!0,c=!0;if(typeof e!="function")throw new TypeError(Ka);return Oe(s)&&(d="leading"in s?!!s.leading:d,c="trailing"in s?!!s.trailing:c),Xa(e,l,{leading:d,maxWait:l,trailing:c})}const zt=be({name:"Add",render(){return f("svg",{width:"512",height:"512",viewBox:"0 0 512 512",fill:"none",xmlns:"http://www.w3.org/2000/svg"},f("path",{d:"M256 112V400M400 256H112",stroke:"currentColor","stroke-width":"32","stroke-linecap":"round","stroke-linejoin":"round"}))}}),qa=be({name:"Remove",render(){return f("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 512 512"},f("line",{x1:"400",y1:"256",x2:"112",y2:"256",style:`
        fill: none;
        stroke: currentColor;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-width: 32px;
      `}))}}),Qa={paddingSmall:"12px 16px 12px",paddingMedium:"19px 24px 20px",paddingLarge:"23px 32px 24px",paddingHuge:"27px 40px 28px",titleFontSizeSmall:"16px",titleFontSizeMedium:"18px",titleFontSizeLarge:"18px",titleFontSizeHuge:"18px",closeIconSize:"18px",closeSize:"22px"};function Za(e){const{primaryColor:l,borderRadius:s,lineHeight:d,fontSize:c,cardColor:C,textColor2:h,textColor1:i,dividerColor:w,fontWeightStrong:z,closeIconColor:p,closeIconColorHover:u,closeIconColorPressed:L,closeColorHover:I,closeColorPressed:_,modalColor:F,boxShadow1:k,popoverColor:O,actionColor:E}=e;return Object.assign(Object.assign({},Qa),{lineHeight:d,color:C,colorModal:F,colorPopover:O,colorTarget:l,colorEmbedded:E,colorEmbeddedModal:E,colorEmbeddedPopover:E,textColor:h,titleTextColor:i,borderColor:w,actionColor:E,titleFontWeight:z,closeColorHover:I,closeColorPressed:_,closeBorderRadius:s,closeIconColor:p,closeIconColorHover:u,closeIconColorPressed:L,fontSizeSmall:c,fontSizeMedium:c,fontSizeLarge:c,fontSizeHuge:c,boxShadow:k,borderRadius:s})}const en={common:Qe,self:Za},ut=o("card-content",`
 flex: 1;
 min-width: 0;
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
`),tn=m([o("card",`
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
 `,[Zt({background:"var(--n-color-modal)"}),v("hoverable",[m("&:hover","box-shadow: var(--n-box-shadow);")]),v("content-segmented",[m(">",[o("card-content",`
 padding-top: var(--n-padding-bottom);
 `),M("content-scrollbar",[m(">",[o("scrollbar-container",[m(">",[o("card-content",`
 padding-top: var(--n-padding-bottom);
 `)])])])])])]),v("content-soft-segmented",[m(">",[o("card-content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `),M("content-scrollbar",[m(">",[o("scrollbar-container",[m(">",[o("card-content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `)])])])])])]),v("footer-segmented",[m(">",[M("footer",`
 padding-top: var(--n-padding-bottom);
 `)])]),v("footer-soft-segmented",[m(">",[M("footer",`
 padding: var(--n-padding-bottom) 0;
 margin: 0 var(--n-padding-left);
 `)])]),m(">",[o("card-header",`
 box-sizing: border-box;
 display: flex;
 align-items: center;
 font-size: var(--n-title-font-size);
 padding:
 var(--n-padding-top)
 var(--n-padding-left)
 var(--n-padding-bottom)
 var(--n-padding-left);
 `,[M("main",`
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 flex: 1;
 min-width: 0;
 color: var(--n-title-text-color);
 `),M("extra",`
 display: flex;
 align-items: center;
 font-size: var(--n-font-size);
 font-weight: 400;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 `),M("close",`
 margin: 0 0 0 8px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `)]),M("action",`
 box-sizing: border-box;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 background-clip: padding-box;
 background-color: var(--n-action-color);
 `),ut,o("card-content",[m("&:first-child",`
 padding-top: var(--n-padding-bottom);
 `)]),M("content-scrollbar",`
 display: flex;
 flex-direction: column;
 `,[m(">",[o("scrollbar-container",[m(">",[ut])])]),m("&:first-child >",[o("scrollbar-container",[m(">",[o("card-content",`
 padding-top: var(--n-padding-bottom);
 `)])])])]),M("footer",`
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
 `,[m("&:first-child",`
 padding-top: var(--n-padding-bottom);
 `)]),M("action",`
 background-color: var(--n-action-color);
 padding: var(--n-padding-bottom) var(--n-padding-left);
 border-bottom-left-radius: var(--n-border-radius);
 border-bottom-right-radius: var(--n-border-radius);
 `)]),o("card-cover",`
 overflow: hidden;
 width: 100%;
 border-radius: var(--n-border-radius) var(--n-border-radius) 0 0;
 `,[m("img",`
 display: block;
 width: 100%;
 `)]),v("bordered",`
 border: 1px solid var(--n-border-color);
 `,[m("&:target","border-color: var(--n-color-target);")]),v("action-segmented",[m(">",[M("action",[m("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),v("content-segmented, content-soft-segmented",[m(">",[o("card-content",`
 transition: border-color 0.3s var(--n-bezier);
 `,[m("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)]),M("content-scrollbar",`
 transition: border-color 0.3s var(--n-bezier);
 `,[m("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),v("footer-segmented, footer-soft-segmented",[m(">",[M("footer",`
 transition: border-color 0.3s var(--n-bezier);
 `,[m("&:not(:first-child)",`
 border-top: 1px solid var(--n-border-color);
 `)])])]),v("embedded",`
 background-color: var(--n-color-embedded);
 `)]),ea(o("card",`
 background: var(--n-color-modal);
 `,[v("embedded",`
 background-color: var(--n-color-embedded-modal);
 `)])),ta(o("card",`
 background: var(--n-color-popover);
 `,[v("embedded",`
 background-color: var(--n-color-embedded-popover);
 `)]))]),an={title:[String,Function],contentClass:String,contentStyle:[Object,String],contentScrollable:Boolean,headerClass:String,headerStyle:[Object,String],headerExtraClass:String,headerExtraStyle:[Object,String],footerClass:String,footerStyle:[Object,String],embedded:Boolean,segmented:{type:[Boolean,Object],default:!1},size:String,bordered:{type:Boolean,default:!0},closable:Boolean,hoverable:Boolean,role:String,onClose:[Function,Array],tag:{type:String,default:"div"},cover:Function,content:[String,Function],footer:Function,action:Function,headerExtra:Function,closeFocusable:Boolean},nn=Object.assign(Object.assign({},we.props),an),Ve=be({name:"Card",props:nn,slots:Object,setup(e){const l=()=>{const{onClose:u}=e;u&&Z(u)},{inlineThemeDisabled:s,mergedClsPrefixRef:d,mergedRtlRef:c,mergedComponentPropsRef:C}=Ze(e),h=we("Card","-card",tn,en,e,d),i=ht("Card",c,d),w=G(()=>{var u,L;return e.size||((L=(u=C==null?void 0:C.value)===null||u===void 0?void 0:u.Card)===null||L===void 0?void 0:L.size)||"medium"}),z=G(()=>{const u=w.value,{self:{color:L,colorModal:I,colorTarget:_,textColor:F,titleTextColor:k,titleFontWeight:O,borderColor:E,actionColor:J,borderRadius:H,lineHeight:$,closeIconColor:x,closeIconColorHover:B,closeIconColorPressed:a,closeColorHover:S,closeColorPressed:R,closeBorderRadius:q,closeIconSize:le,closeSize:ee,boxShadow:he,colorPopover:ie,colorEmbedded:fe,colorEmbeddedModal:X,colorEmbeddedPopover:pe,[K("padding",u)]:ze,[K("fontSize",u)]:Te,[K("titleFontSize",u)]:ve},common:{cubicBezierEaseInOut:xe}}=h.value,{top:Re,left:ne,bottom:oe}=$e(ze);return{"--n-bezier":xe,"--n-border-radius":H,"--n-color":L,"--n-color-modal":I,"--n-color-popover":ie,"--n-color-embedded":fe,"--n-color-embedded-modal":X,"--n-color-embedded-popover":pe,"--n-color-target":_,"--n-text-color":F,"--n-line-height":$,"--n-action-color":J,"--n-title-text-color":k,"--n-title-font-weight":O,"--n-close-icon-color":x,"--n-close-icon-color-hover":B,"--n-close-icon-color-pressed":a,"--n-close-color-hover":S,"--n-close-color-pressed":R,"--n-border-color":E,"--n-box-shadow":he,"--n-padding-top":Re,"--n-padding-bottom":oe,"--n-padding-left":ne,"--n-font-size":Te,"--n-title-font-size":ve,"--n-close-size":ee,"--n-close-icon-size":le,"--n-close-border-radius":q}}),p=s?xt("card",G(()=>w.value[0]),z,e):void 0;return{rtlEnabled:i,mergedClsPrefix:d,mergedTheme:h,handleCloseClick:l,cssVars:s?void 0:z,themeClass:p==null?void 0:p.themeClass,onRender:p==null?void 0:p.onRender}},render(){const{segmented:e,bordered:l,hoverable:s,mergedClsPrefix:d,rtlEnabled:c,onRender:C,embedded:h,tag:i,$slots:w}=this;return C==null||C(),f(i,{class:[`${d}-card`,this.themeClass,h&&`${d}-card--embedded`,{[`${d}-card--rtl`]:c,[`${d}-card--content-scrollable`]:this.contentScrollable,[`${d}-card--content${typeof e!="boolean"&&e.content==="soft"?"-soft":""}-segmented`]:e===!0||e!==!1&&e.content,[`${d}-card--footer${typeof e!="boolean"&&e.footer==="soft"?"-soft":""}-segmented`]:e===!0||e!==!1&&e.footer,[`${d}-card--action-segmented`]:e===!0||e!==!1&&e.action,[`${d}-card--bordered`]:l,[`${d}-card--hoverable`]:s}],style:this.cssVars,role:this.role},ae(w.cover,z=>{const p=this.cover?Ce([this.cover()]):z;return p&&f("div",{class:`${d}-card-cover`,role:"none"},p)}),ae(w.header,z=>{const{title:p}=this,u=p?Ce(typeof p=="function"?[p()]:[p]):z;return u||this.closable?f("div",{class:[`${d}-card-header`,this.headerClass],style:this.headerStyle,role:"heading"},f("div",{class:`${d}-card-header__main`,role:"heading"},u),ae(w["header-extra"],L=>{const I=this.headerExtra?Ce([this.headerExtra()]):L;return I&&f("div",{class:[`${d}-card-header__extra`,this.headerExtraClass],style:this.headerExtraStyle},I)}),this.closable&&f(yt,{clsPrefix:d,class:`${d}-card-header__close`,onClick:this.handleCloseClick,focusable:this.closeFocusable,absolute:!0})):null}),ae(w.default,z=>{const{content:p}=this,u=p?Ce(typeof p=="function"?[p()]:[p]):z;return u?this.contentScrollable?f(aa,{class:`${d}-card__content-scrollbar`,contentClass:[`${d}-card-content`,this.contentClass],contentStyle:this.contentStyle},u):f("div",{class:[`${d}-card-content`,this.contentClass],style:this.contentStyle,role:"none"},u):null}),ae(w.footer,z=>{const p=this.footer?Ce([this.footer()]):z;return p&&f("div",{class:[`${d}-card__footer`,this.footerClass],style:this.footerStyle,role:"none"},p)}),ae(w.action,z=>{const p=this.action?Ce([this.action()]):z;return p&&f("div",{class:`${d}-card__action`,role:"none"},p)}))}});function on(){const e=St(oa,null);return e===null&&na("use-message","No outer <n-message-provider /> founded. See prerequisite in https://www.naiveui.com/en-US/os-theme/components/message for more details. If you want to use `useMessage` outside setup, please check https://www.naiveui.com/zh-CN/os-theme/components/message#Q-&-A."),e}function rn(e){const{textColorDisabled:l}=e;return{iconColorDisabled:l}}const ln=ra({name:"InputNumber",common:Qe,peers:{Button:ka,Input:Va},self:rn}),sn={tabFontSizeSmall:"14px",tabFontSizeMedium:"14px",tabFontSizeLarge:"16px",tabGapSmallLine:"36px",tabGapMediumLine:"36px",tabGapLargeLine:"36px",tabGapSmallLineVertical:"8px",tabGapMediumLineVertical:"8px",tabGapLargeLineVertical:"8px",tabPaddingSmallLine:"6px 0",tabPaddingMediumLine:"10px 0",tabPaddingLargeLine:"14px 0",tabPaddingVerticalSmallLine:"6px 12px",tabPaddingVerticalMediumLine:"8px 16px",tabPaddingVerticalLargeLine:"10px 20px",tabGapSmallBar:"36px",tabGapMediumBar:"36px",tabGapLargeBar:"36px",tabGapSmallBarVertical:"8px",tabGapMediumBarVertical:"8px",tabGapLargeBarVertical:"8px",tabPaddingSmallBar:"4px 0",tabPaddingMediumBar:"6px 0",tabPaddingLargeBar:"10px 0",tabPaddingVerticalSmallBar:"6px 12px",tabPaddingVerticalMediumBar:"8px 16px",tabPaddingVerticalLargeBar:"10px 20px",tabGapSmallCard:"4px",tabGapMediumCard:"4px",tabGapLargeCard:"4px",tabGapSmallCardVertical:"4px",tabGapMediumCardVertical:"4px",tabGapLargeCardVertical:"4px",tabPaddingSmallCard:"8px 16px",tabPaddingMediumCard:"10px 20px",tabPaddingLargeCard:"12px 24px",tabPaddingSmallSegment:"4px 0",tabPaddingMediumSegment:"6px 0",tabPaddingLargeSegment:"8px 0",tabPaddingVerticalLargeSegment:"0 8px",tabPaddingVerticalSmallCard:"8px 12px",tabPaddingVerticalMediumCard:"10px 16px",tabPaddingVerticalLargeCard:"12px 20px",tabPaddingVerticalSmallSegment:"0 4px",tabPaddingVerticalMediumSegment:"0 6px",tabGapSmallSegment:"0",tabGapMediumSegment:"0",tabGapLargeSegment:"0",tabGapSmallSegmentVertical:"0",tabGapMediumSegmentVertical:"0",tabGapLargeSegmentVertical:"0",panePaddingSmall:"8px 0 0 0",panePaddingMedium:"12px 0 0 0",panePaddingLarge:"16px 0 0 0",closeSize:"18px",closeIconSize:"14px"};function dn(e){const{textColor2:l,primaryColor:s,textColorDisabled:d,closeIconColor:c,closeIconColorHover:C,closeIconColorPressed:h,closeColorHover:i,closeColorPressed:w,tabColor:z,baseColor:p,dividerColor:u,fontWeight:L,textColor1:I,borderRadius:_,fontSize:F,fontWeightStrong:k}=e;return Object.assign(Object.assign({},sn),{colorSegment:z,tabFontSizeCard:F,tabTextColorLine:I,tabTextColorActiveLine:s,tabTextColorHoverLine:s,tabTextColorDisabledLine:d,tabTextColorSegment:I,tabTextColorActiveSegment:l,tabTextColorHoverSegment:l,tabTextColorDisabledSegment:d,tabTextColorBar:I,tabTextColorActiveBar:s,tabTextColorHoverBar:s,tabTextColorDisabledBar:d,tabTextColorCard:I,tabTextColorHoverCard:I,tabTextColorActiveCard:s,tabTextColorDisabledCard:d,barColor:s,closeIconColor:c,closeIconColorHover:C,closeIconColorPressed:h,closeColorHover:i,closeColorPressed:w,closeBorderRadius:_,tabColor:z,tabColorSegment:p,tabBorderColor:u,tabFontWeightActive:L,tabFontWeight:L,tabBorderRadius:_,paneTextColor:l,fontWeightStrong:k})}const cn={common:Qe,self:dn},un=m([o("input-number-suffix",`
 display: inline-block;
 margin-right: 10px;
 `),o("input-number-prefix",`
 display: inline-block;
 margin-left: 10px;
 `)]);function bn(e){return e==null||typeof e=="string"&&e.trim()===""?null:Number(e)}function fn(e){return e.includes(".")&&(/^(-)?\d+.*(\.|0)$/.test(e)||/^-?\d*$/.test(e))||e==="-"||e==="-0"}function Je(e){return e==null?!0:!Number.isNaN(e)}function bt(e,l){return typeof e!="number"?"":l===void 0?String(e):e.toFixed(l)}function Xe(e){if(e===null)return null;if(typeof e=="number")return e;{const l=Number(e);return Number.isNaN(l)?null:l}}const ft=800,pt=100,pn=Object.assign(Object.assign({},we.props),{autofocus:Boolean,loading:{type:Boolean,default:void 0},placeholder:String,defaultValue:{type:Number,default:null},value:Number,step:{type:[Number,String],default:1},min:[Number,String],max:[Number,String],size:String,disabled:{type:Boolean,default:void 0},validator:Function,bordered:{type:Boolean,default:void 0},showButton:{type:Boolean,default:!0},buttonPlacement:{type:String,default:"right"},inputProps:Object,readonly:Boolean,clearable:Boolean,keyboard:{type:Object,default:{}},updateValueOnInput:{type:Boolean,default:!0},round:{type:Boolean,default:void 0},parse:Function,format:Function,precision:Number,status:String,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onFocus:[Function,Array],onBlur:[Function,Array],onClear:[Function,Array],onChange:[Function,Array]}),vn=be({name:"InputNumber",props:pn,slots:Object,setup(e){const{mergedBorderedRef:l,mergedClsPrefixRef:s,mergedRtlRef:d,mergedComponentPropsRef:c}=Ze(e),C=we("InputNumber","-input-number",un,ln,e,s),{localeRef:h}=la("InputNumber"),i=ia(e,{mergedSize:r=>{var g,P;const{size:A}=e;if(A)return A;const{mergedSize:t}=r||{};if(t!=null&&t.value)return t.value;const n=(P=(g=c==null?void 0:c.value)===null||g===void 0?void 0:g.InputNumber)===null||P===void 0?void 0:P.size;return n||"medium"}}),{mergedSizeRef:w,mergedDisabledRef:z,mergedStatusRef:p}=i,u=j(null),L=j(null),I=j(null),_=j(e.defaultValue),F=Q(e,"value"),k=Ct(F,_),O=j(""),E=r=>{const g=String(r).split(".")[1];return g?g.length:0},J=r=>{const g=[e.min,e.max,e.step,r].map(P=>P===void 0?0:E(P));return Math.max(...g)},H=me(()=>{const{placeholder:r}=e;return r!==void 0?r:h.value.placeholder}),$=me(()=>{const r=Xe(e.step);return r!==null?r===0?1:Math.abs(r):1}),x=me(()=>{const r=Xe(e.min);return r!==null?r:null}),B=me(()=>{const r=Xe(e.max);return r!==null?r:null}),a=()=>{const{value:r}=k;if(Je(r)){const{format:g,precision:P}=e;g?O.value=g(r):r===null||P===void 0||E(r)>P?O.value=bt(r,void 0):O.value=bt(r,P)}else O.value=String(r)};a();const S=r=>{const{value:g}=k;if(r===g){a();return}const{"onUpdate:value":P,onUpdateValue:A,onChange:t}=e,{nTriggerFormInput:n,nTriggerFormChange:b}=i;t&&Z(t,r),A&&Z(A,r),P&&Z(P,r),_.value=r,n(),b()},R=({offset:r,doUpdateIfValid:g,fixPrecision:P,isInputing:A})=>{const{value:t}=O;if(A&&fn(t))return!1;const n=(e.parse||bn)(t);if(n===null)return g&&S(null),null;if(Je(n)){const b=E(n),{precision:T}=e;if(T!==void 0&&T<b&&!P)return!1;let N=Number.parseFloat((n+r).toFixed(T??J(n)));if(Je(N)){const{value:D}=B,{value:U}=x;if(D!==null&&N>D){if(!g||A)return!1;N=D}if(U!==null&&N<U){if(!g||A)return!1;N=U}return e.validator&&!e.validator(N)?!1:(g&&S(N),N)}}return!1},q=me(()=>R({offset:0,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})===!1),le=me(()=>{const{value:r}=k;if(e.validator&&r===null)return!1;const{value:g}=$;return R({offset:-g,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})!==!1}),ee=me(()=>{const{value:r}=k;if(e.validator&&r===null)return!1;const{value:g}=$;return R({offset:+g,doUpdateIfValid:!1,isInputing:!1,fixPrecision:!1})!==!1});function he(r){const{onFocus:g}=e,{nTriggerFormFocus:P}=i;g&&Z(g,r),P()}function ie(r){var g,P;if(r.target===((g=u.value)===null||g===void 0?void 0:g.wrapperElRef))return;const A=R({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0});if(A!==!1){const b=(P=u.value)===null||P===void 0?void 0:P.inputElRef;b&&(b.value=String(A||"")),k.value===A&&a()}else a();const{onBlur:t}=e,{nTriggerFormBlur:n}=i;t&&Z(t,r),n(),Le(()=>{a()})}function fe(r){const{onClear:g}=e;g&&Z(g,r)}function X(){const{value:r}=ee;if(!r){ye();return}const{value:g}=k;if(g===null)e.validator||S(ve());else{const{value:P}=$;R({offset:P,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})}}function pe(){const{value:r}=le;if(!r){te();return}const{value:g}=k;if(g===null)e.validator||S(ve());else{const{value:P}=$;R({offset:-P,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})}}const ze=he,Te=ie;function ve(){if(e.validator)return null;const{value:r}=x,{value:g}=B;return r!==null?Math.max(0,r):g!==null?Math.min(0,g):0}function xe(r){fe(r),S(null)}function Re(r){var g,P,A;!((g=I.value)===null||g===void 0)&&g.$el.contains(r.target)&&r.preventDefault(),!((P=L.value)===null||P===void 0)&&P.$el.contains(r.target)&&r.preventDefault(),(A=u.value)===null||A===void 0||A.activate()}let ne=null,oe=null,ge=null;function te(){ge&&(window.clearTimeout(ge),ge=null),ne&&(window.clearInterval(ne),ne=null)}let se=null;function ye(){se&&(window.clearTimeout(se),se=null),oe&&(window.clearInterval(oe),oe=null)}function Ae(){te(),ge=window.setTimeout(()=>{ne=window.setInterval(()=>{pe()},pt)},ft),at("mouseup",document,te,{once:!0})}function Ne(){ye(),se=window.setTimeout(()=>{oe=window.setInterval(()=>{X()},pt)},ft),at("mouseup",document,ye,{once:!0})}const de=()=>{oe||X()},Fe=()=>{ne||pe()};function We(r){var g,P;if(r.key==="Enter"){if(r.target===((g=u.value)===null||g===void 0?void 0:g.wrapperElRef))return;R({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&((P=u.value)===null||P===void 0||P.deactivate())}else if(r.key==="ArrowUp"){if(!ee.value||e.keyboard.ArrowUp===!1)return;r.preventDefault(),R({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&X()}else if(r.key==="ArrowDown"){if(!le.value||e.keyboard.ArrowDown===!1)return;r.preventDefault(),R({offset:0,doUpdateIfValid:!0,isInputing:!1,fixPrecision:!0})!==!1&&pe()}}function je(r){O.value=r,e.updateValueOnInput&&!e.format&&!e.parse&&e.precision===void 0&&R({offset:0,doUpdateIfValid:!0,isInputing:!0,fixPrecision:!1})}ke(k,()=>{a()});const Pe={focus:()=>{var r;return(r=u.value)===null||r===void 0?void 0:r.focus()},blur:()=>{var r;return(r=u.value)===null||r===void 0?void 0:r.blur()},select:()=>{var r;return(r=u.value)===null||r===void 0?void 0:r.select()}},He=ht("InputNumber",d,s);return Object.assign(Object.assign({},Pe),{rtlEnabled:He,inputInstRef:u,minusButtonInstRef:L,addButtonInstRef:I,mergedClsPrefix:s,mergedBordered:l,uncontrolledValue:_,mergedValue:k,mergedPlaceholder:H,displayedValueInvalid:q,mergedSize:w,mergedDisabled:z,displayedValue:O,addable:ee,minusable:le,mergedStatus:p,handleFocus:ze,handleBlur:Te,handleClear:xe,handleMouseDown:Re,handleAddClick:de,handleMinusClick:Fe,handleAddMousedown:Ne,handleMinusMousedown:Ae,handleKeyDown:We,handleUpdateDisplayedValue:je,mergedTheme:C,inputThemeOverrides:{paddingSmall:"0 8px 0 10px",paddingMedium:"0 8px 0 12px",paddingLarge:"0 8px 0 14px"},buttonThemeOverrides:G(()=>{const{self:{iconColorDisabled:r}}=C.value,[g,P,A,t]=sa(r);return{textColorTextDisabled:`rgb(${g}, ${P}, ${A})`,opacityDisabled:`${t}`}})})},render(){const{mergedClsPrefix:e,$slots:l}=this,s=()=>f(it,{text:!0,disabled:!this.minusable||this.mergedDisabled||this.readonly,focusable:!1,theme:this.mergedTheme.peers.Button,themeOverrides:this.mergedTheme.peerOverrides.Button,builtinThemeOverrides:this.buttonThemeOverrides,onClick:this.handleMinusClick,onMousedown:this.handleMinusMousedown,ref:"minusButtonInstRef"},{icon:()=>tt(l["minus-icon"],()=>[f(qe,{clsPrefix:e},{default:()=>f(qa,null)})])}),d=()=>f(it,{text:!0,disabled:!this.addable||this.mergedDisabled||this.readonly,focusable:!1,theme:this.mergedTheme.peers.Button,themeOverrides:this.mergedTheme.peerOverrides.Button,builtinThemeOverrides:this.buttonThemeOverrides,onClick:this.handleAddClick,onMousedown:this.handleAddMousedown,ref:"addButtonInstRef"},{icon:()=>tt(l["add-icon"],()=>[f(qe,{clsPrefix:e},{default:()=>f(zt,null)})])});return f("div",{class:[`${e}-input-number`,this.rtlEnabled&&`${e}-input-number--rtl`]},f(Y,{ref:"inputInstRef",autofocus:this.autofocus,status:this.mergedStatus,bordered:this.mergedBordered,loading:this.loading,value:this.displayedValue,onUpdateValue:this.handleUpdateDisplayedValue,theme:this.mergedTheme.peers.Input,themeOverrides:this.mergedTheme.peerOverrides.Input,builtinThemeOverrides:this.inputThemeOverrides,size:this.mergedSize,placeholder:this.mergedPlaceholder,disabled:this.mergedDisabled,readonly:this.readonly,round:this.round,textDecoration:this.displayedValueInvalid?"line-through":void 0,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeydown:this.handleKeyDown,onMousedown:this.handleMouseDown,onClear:this.handleClear,clearable:this.clearable,inputProps:this.inputProps,internalLoadingBeforeSuffix:!0},{prefix:()=>{var c;return this.showButton&&this.buttonPlacement==="both"?[s(),ae(l.prefix,C=>C?f("span",{class:`${e}-input-number-prefix`},C):null)]:(c=l.prefix)===null||c===void 0?void 0:c.call(l)},suffix:()=>{var c;return this.showButton?[ae(l.suffix,C=>C?f("span",{class:`${e}-input-number-suffix`},C):null),this.buttonPlacement==="right"?s():null,d()]:(c=l.suffix)===null||c===void 0?void 0:c.call(l)}}))}}),Tt=da("n-tabs"),gn={tab:[String,Number,Object,Function],name:{type:[String,Number],required:!0},disabled:Boolean,displayDirective:{type:String,default:"if"},closable:{type:Boolean,default:void 0},tabProps:Object,label:[String,Number,Object,Function]},mn=Object.assign({internalLeftPadded:Boolean,internalAddable:Boolean,internalCreatedByPane:Boolean},ba(gn,["displayDirective"])),Ee=be({__TAB__:!0,inheritAttrs:!1,name:"Tab",props:mn,setup(e){const{mergedClsPrefixRef:l,valueRef:s,typeRef:d,closableRef:c,tabStyleRef:C,addTabStyleRef:h,tabClassRef:i,addTabClassRef:w,tabChangeIdRef:z,onBeforeLeaveRef:p,triggerRef:u,handleAdd:L,activateTab:I,handleClose:_}=St(Tt);return{trigger:u,mergedClosable:G(()=>{if(e.internalAddable)return!1;const{closable:F}=e;return F===void 0?c.value:F}),style:C,addStyle:h,tabClass:i,addTabClass:w,clsPrefix:l,value:s,type:d,handleClose(F){F.stopPropagation(),!e.disabled&&_(e.name)},activateTab(){if(e.disabled)return;if(e.internalAddable){L();return}const{name:F}=e,k=++z.id;if(F!==s.value){const{value:O}=p;O?Promise.resolve(O(e.name,s.value)).then(E=>{E&&z.id===k&&I(F)}):I(F)}}}},render(){const{internalAddable:e,clsPrefix:l,name:s,disabled:d,label:c,tab:C,value:h,mergedClosable:i,trigger:w,$slots:{default:z}}=this,p=c??C;return f("div",{class:`${l}-tabs-tab-wrapper`},this.internalLeftPadded?f("div",{class:`${l}-tabs-tab-pad`}):null,f("div",Object.assign({key:s,"data-name":s,"data-disabled":d?!0:void 0},ca({class:[`${l}-tabs-tab`,h===s&&`${l}-tabs-tab--active`,d&&`${l}-tabs-tab--disabled`,i&&`${l}-tabs-tab--closable`,e&&`${l}-tabs-tab--addable`,e?this.addTabClass:this.tabClass],onClick:w==="click"?this.activateTab:void 0,onMouseenter:w==="hover"?this.activateTab:void 0,style:e?this.addStyle:this.style},this.internalCreatedByPane?this.tabProps||{}:this.$attrs)),f("span",{class:`${l}-tabs-tab__label`},e?f(Me,null,f("div",{class:`${l}-tabs-tab__height-placeholder`}," "),f(qe,{clsPrefix:l},{default:()=>f(zt,null)})):z?z():typeof p=="object"?p:ua(p??s)),i&&this.type==="card"?f(yt,{clsPrefix:l,class:`${l}-tabs-tab__close`,onClick:this.handleClose,disabled:d}):null))}}),hn=o("tabs",`
 box-sizing: border-box;
 width: 100%;
 display: flex;
 flex-direction: column;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
`,[v("segment-type",[o("tabs-rail",[m("&.transition-disabled",[o("tabs-capsule",`
 transition: none;
 `)])])]),v("top",[o("tab-pane",`
 padding: var(--n-pane-padding-top) var(--n-pane-padding-right) var(--n-pane-padding-bottom) var(--n-pane-padding-left);
 `)]),v("left",[o("tab-pane",`
 padding: var(--n-pane-padding-right) var(--n-pane-padding-bottom) var(--n-pane-padding-left) var(--n-pane-padding-top);
 `)]),v("left, right",`
 flex-direction: row;
 `,[o("tabs-bar",`
 width: 2px;
 right: 0;
 transition:
 top .2s var(--n-bezier),
 max-height .2s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `),o("tabs-tab",`
 padding: var(--n-tab-padding-vertical); 
 `)]),v("right",`
 flex-direction: row-reverse;
 `,[o("tab-pane",`
 padding: var(--n-pane-padding-left) var(--n-pane-padding-top) var(--n-pane-padding-right) var(--n-pane-padding-bottom);
 `),o("tabs-bar",`
 left: 0;
 `)]),v("bottom",`
 flex-direction: column-reverse;
 justify-content: flex-end;
 `,[o("tab-pane",`
 padding: var(--n-pane-padding-bottom) var(--n-pane-padding-right) var(--n-pane-padding-top) var(--n-pane-padding-left);
 `),o("tabs-bar",`
 top: 0;
 `)]),o("tabs-rail",`
 position: relative;
 padding: 3px;
 border-radius: var(--n-tab-border-radius);
 width: 100%;
 background-color: var(--n-color-segment);
 transition: background-color .3s var(--n-bezier);
 display: flex;
 align-items: center;
 `,[o("tabs-capsule",`
 border-radius: var(--n-tab-border-radius);
 position: absolute;
 pointer-events: none;
 background-color: var(--n-tab-color-segment);
 box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .08);
 transition: transform 0.3s var(--n-bezier);
 `),o("tabs-tab-wrapper",`
 flex-basis: 0;
 flex-grow: 1;
 display: flex;
 align-items: center;
 justify-content: center;
 `,[o("tabs-tab",`
 overflow: hidden;
 border-radius: var(--n-tab-border-radius);
 width: 100%;
 display: flex;
 align-items: center;
 justify-content: center;
 `,[v("active",`
 font-weight: var(--n-font-weight-strong);
 color: var(--n-tab-text-color-active);
 `),m("&:hover",`
 color: var(--n-tab-text-color-hover);
 `)])])]),v("flex",[o("tabs-nav",`
 width: 100%;
 position: relative;
 `,[o("tabs-wrapper",`
 width: 100%;
 `,[o("tabs-tab",`
 margin-right: 0;
 `)])])]),o("tabs-nav",`
 box-sizing: border-box;
 line-height: 1.5;
 display: flex;
 transition: border-color .3s var(--n-bezier);
 `,[M("prefix, suffix",`
 display: flex;
 align-items: center;
 `),M("prefix","padding-right: 16px;"),M("suffix","padding-left: 16px;")]),v("top, bottom",[m(">",[o("tabs-nav",[o("tabs-nav-scroll-wrapper",[m("&::before",`
 top: 0;
 bottom: 0;
 left: 0;
 width: 20px;
 `),m("&::after",`
 top: 0;
 bottom: 0;
 right: 0;
 width: 20px;
 `),v("shadow-start",[m("&::before",`
 box-shadow: inset 10px 0 8px -8px rgba(0, 0, 0, .12);
 `)]),v("shadow-end",[m("&::after",`
 box-shadow: inset -10px 0 8px -8px rgba(0, 0, 0, .12);
 `)])])])])]),v("left, right",[o("tabs-nav-scroll-content",`
 flex-direction: column;
 `),m(">",[o("tabs-nav",[o("tabs-nav-scroll-wrapper",[m("&::before",`
 top: 0;
 left: 0;
 right: 0;
 height: 20px;
 `),m("&::after",`
 bottom: 0;
 left: 0;
 right: 0;
 height: 20px;
 `),v("shadow-start",[m("&::before",`
 box-shadow: inset 0 10px 8px -8px rgba(0, 0, 0, .12);
 `)]),v("shadow-end",[m("&::after",`
 box-shadow: inset 0 -10px 8px -8px rgba(0, 0, 0, .12);
 `)])])])])]),o("tabs-nav-scroll-wrapper",`
 flex: 1;
 position: relative;
 overflow: hidden;
 `,[o("tabs-nav-y-scroll",`
 height: 100%;
 width: 100%;
 overflow-y: auto; 
 scrollbar-width: none;
 `,[m("&::-webkit-scrollbar, &::-webkit-scrollbar-track-piece, &::-webkit-scrollbar-thumb",`
 width: 0;
 height: 0;
 display: none;
 `)]),m("&::before, &::after",`
 transition: box-shadow .3s var(--n-bezier);
 pointer-events: none;
 content: "";
 position: absolute;
 z-index: 1;
 `)]),o("tabs-nav-scroll-content",`
 display: flex;
 position: relative;
 min-width: 100%;
 min-height: 100%;
 width: fit-content;
 box-sizing: border-box;
 `),o("tabs-wrapper",`
 display: inline-flex;
 flex-wrap: nowrap;
 position: relative;
 `),o("tabs-tab-wrapper",`
 display: flex;
 flex-wrap: nowrap;
 flex-shrink: 0;
 flex-grow: 0;
 `),o("tabs-tab",`
 cursor: pointer;
 white-space: nowrap;
 flex-wrap: nowrap;
 display: inline-flex;
 align-items: center;
 color: var(--n-tab-text-color);
 font-size: var(--n-tab-font-size);
 background-clip: padding-box;
 padding: var(--n-tab-padding);
 transition:
 box-shadow .3s var(--n-bezier),
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[v("disabled",{cursor:"not-allowed"}),M("close",`
 margin-left: 6px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `),M("label",`
 display: flex;
 align-items: center;
 z-index: 1;
 `)]),o("tabs-bar",`
 position: absolute;
 bottom: 0;
 height: 2px;
 border-radius: 1px;
 background-color: var(--n-bar-color);
 transition:
 left .2s var(--n-bezier),
 max-width .2s var(--n-bezier),
 opacity .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `,[m("&.transition-disabled",`
 transition: none;
 `),v("disabled",`
 background-color: var(--n-tab-text-color-disabled)
 `)]),o("tabs-pane-wrapper",`
 position: relative;
 overflow: hidden;
 transition: max-height .2s var(--n-bezier);
 `),o("tab-pane",`
 color: var(--n-pane-text-color);
 width: 100%;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 opacity .2s var(--n-bezier);
 left: 0;
 right: 0;
 top: 0;
 `,[m("&.next-transition-leave-active, &.prev-transition-leave-active, &.next-transition-enter-active, &.prev-transition-enter-active",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 transform .2s var(--n-bezier),
 opacity .2s var(--n-bezier);
 `),m("&.next-transition-leave-active, &.prev-transition-leave-active",`
 position: absolute;
 `),m("&.next-transition-enter-from, &.prev-transition-leave-to",`
 transform: translateX(32px);
 opacity: 0;
 `),m("&.next-transition-leave-to, &.prev-transition-enter-from",`
 transform: translateX(-32px);
 opacity: 0;
 `),m("&.next-transition-leave-from, &.next-transition-enter-to, &.prev-transition-leave-from, &.prev-transition-enter-to",`
 transform: translateX(0);
 opacity: 1;
 `)]),o("tabs-tab-pad",`
 box-sizing: border-box;
 width: var(--n-tab-gap);
 flex-grow: 0;
 flex-shrink: 0;
 `),v("line-type, bar-type",[o("tabs-tab",`
 font-weight: var(--n-tab-font-weight);
 box-sizing: border-box;
 vertical-align: bottom;
 `,[m("&:hover",{color:"var(--n-tab-text-color-hover)"}),v("active",`
 color: var(--n-tab-text-color-active);
 font-weight: var(--n-tab-font-weight-active);
 `),v("disabled",{color:"var(--n-tab-text-color-disabled)"})])]),o("tabs-nav",[v("line-type",[v("top",[M("prefix, suffix",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),o("tabs-nav-scroll-content",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),o("tabs-bar",`
 bottom: -1px;
 `)]),v("left",[M("prefix, suffix",`
 border-right: 1px solid var(--n-tab-border-color);
 `),o("tabs-nav-scroll-content",`
 border-right: 1px solid var(--n-tab-border-color);
 `),o("tabs-bar",`
 right: -1px;
 `)]),v("right",[M("prefix, suffix",`
 border-left: 1px solid var(--n-tab-border-color);
 `),o("tabs-nav-scroll-content",`
 border-left: 1px solid var(--n-tab-border-color);
 `),o("tabs-bar",`
 left: -1px;
 `)]),v("bottom",[M("prefix, suffix",`
 border-top: 1px solid var(--n-tab-border-color);
 `),o("tabs-nav-scroll-content",`
 border-top: 1px solid var(--n-tab-border-color);
 `),o("tabs-bar",`
 top: -1px;
 `)]),M("prefix, suffix",`
 transition: border-color .3s var(--n-bezier);
 `),o("tabs-nav-scroll-content",`
 transition: border-color .3s var(--n-bezier);
 `),o("tabs-bar",`
 border-radius: 0;
 `)]),v("card-type",[M("prefix, suffix",`
 transition: border-color .3s var(--n-bezier);
 `),o("tabs-pad",`
 flex-grow: 1;
 transition: border-color .3s var(--n-bezier);
 `),o("tabs-tab-pad",`
 transition: border-color .3s var(--n-bezier);
 `),o("tabs-tab",`
 font-weight: var(--n-tab-font-weight);
 border: 1px solid var(--n-tab-border-color);
 background-color: var(--n-tab-color);
 box-sizing: border-box;
 position: relative;
 vertical-align: bottom;
 display: flex;
 justify-content: space-between;
 font-size: var(--n-tab-font-size);
 color: var(--n-tab-text-color);
 `,[v("addable",`
 padding-left: 8px;
 padding-right: 8px;
 font-size: 16px;
 justify-content: center;
 `,[M("height-placeholder",`
 width: 0;
 font-size: var(--n-tab-font-size);
 `),fa("disabled",[m("&:hover",`
 color: var(--n-tab-text-color-hover);
 `)])]),v("closable","padding-right: 8px;"),v("active",`
 background-color: #0000;
 font-weight: var(--n-tab-font-weight-active);
 color: var(--n-tab-text-color-active);
 `),v("disabled","color: var(--n-tab-text-color-disabled);")])]),v("left, right",`
 flex-direction: column; 
 `,[M("prefix, suffix",`
 padding: var(--n-tab-padding-vertical);
 `),o("tabs-wrapper",`
 flex-direction: column;
 `),o("tabs-tab-wrapper",`
 flex-direction: column;
 `,[o("tabs-tab-pad",`
 height: var(--n-tab-gap-vertical);
 width: 100%;
 `)])]),v("top",[v("card-type",[o("tabs-scroll-padding","border-bottom: 1px solid var(--n-tab-border-color);"),M("prefix, suffix",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),o("tabs-tab",`
 border-top-left-radius: var(--n-tab-border-radius);
 border-top-right-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-bottom: 1px solid #0000;
 `)]),o("tabs-tab-pad",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),o("tabs-pad",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `)])]),v("left",[v("card-type",[o("tabs-scroll-padding","border-right: 1px solid var(--n-tab-border-color);"),M("prefix, suffix",`
 border-right: 1px solid var(--n-tab-border-color);
 `),o("tabs-tab",`
 border-top-left-radius: var(--n-tab-border-radius);
 border-bottom-left-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-right: 1px solid #0000;
 `)]),o("tabs-tab-pad",`
 border-right: 1px solid var(--n-tab-border-color);
 `),o("tabs-pad",`
 border-right: 1px solid var(--n-tab-border-color);
 `)])]),v("right",[v("card-type",[o("tabs-scroll-padding","border-left: 1px solid var(--n-tab-border-color);"),M("prefix, suffix",`
 border-left: 1px solid var(--n-tab-border-color);
 `),o("tabs-tab",`
 border-top-right-radius: var(--n-tab-border-radius);
 border-bottom-right-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-left: 1px solid #0000;
 `)]),o("tabs-tab-pad",`
 border-left: 1px solid var(--n-tab-border-color);
 `),o("tabs-pad",`
 border-left: 1px solid var(--n-tab-border-color);
 `)])]),v("bottom",[v("card-type",[o("tabs-scroll-padding","border-top: 1px solid var(--n-tab-border-color);"),M("prefix, suffix",`
 border-top: 1px solid var(--n-tab-border-color);
 `),o("tabs-tab",`
 border-bottom-left-radius: var(--n-tab-border-radius);
 border-bottom-right-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-top: 1px solid #0000;
 `)]),o("tabs-tab-pad",`
 border-top: 1px solid var(--n-tab-border-color);
 `),o("tabs-pad",`
 border-top: 1px solid var(--n-tab-border-color);
 `)])])])]),Ke=Ya,xn=Object.assign(Object.assign({},we.props),{value:[String,Number],defaultValue:[String,Number],trigger:{type:String,default:"click"},type:{type:String,default:"bar"},closable:Boolean,justifyContent:String,size:String,placement:{type:String,default:"top"},tabStyle:[String,Object],tabClass:String,addTabStyle:[String,Object],addTabClass:String,barWidth:Number,paneClass:String,paneStyle:[String,Object],paneWrapperClass:String,paneWrapperStyle:[String,Object],addable:[Boolean,Object],tabsPadding:{type:Number,default:0},animated:Boolean,onBeforeLeave:Function,onAdd:Function,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onClose:[Function,Array],labelSize:String,activeName:[String,Number],onActiveNameChange:[Function,Array]}),yn=be({name:"Tabs",props:xn,slots:Object,setup(e,{slots:l}){var s,d,c,C;const{mergedClsPrefixRef:h,inlineThemeDisabled:i,mergedComponentPropsRef:w}=Ze(e),z=we("Tabs","-tabs",hn,cn,e,h),p=j(null),u=j(null),L=j(null),I=j(null),_=j(null),F=j(null),k=j(!0),O=j(!0),E=nt(e,["labelSize","size"]),J=G(()=>{var t,n;if(E.value)return E.value;const b=(n=(t=w==null?void 0:w.value)===null||t===void 0?void 0:t.Tabs)===null||n===void 0?void 0:n.size;return b||"medium"}),H=nt(e,["activeName","value"]),$=j((d=(s=H.value)!==null&&s!==void 0?s:e.defaultValue)!==null&&d!==void 0?d:l.default?(C=(c=De(l.default())[0])===null||c===void 0?void 0:c.props)===null||C===void 0?void 0:C.name:null),x=Ct(H,$),B={id:0},a=G(()=>{if(!(!e.justifyContent||e.type==="card"))return{display:"flex",justifyContent:e.justifyContent}});ke(x,()=>{B.id=0,ee(),he()});function S(){var t;const{value:n}=x;return n===null?null:(t=p.value)===null||t===void 0?void 0:t.querySelector(`[data-name="${n}"]`)}function R(t){if(e.type==="card")return;const{value:n}=u;if(!n)return;const b=n.style.opacity==="0";if(t){const T=`${h.value}-tabs-bar--disabled`,{barWidth:N,placement:D}=e;if(t.dataset.disabled==="true"?n.classList.add(T):n.classList.remove(T),["top","bottom"].includes(D)){if(le(["top","maxHeight","height"]),typeof N=="number"&&t.offsetWidth>=N){const U=Math.floor((t.offsetWidth-N)/2)+t.offsetLeft;n.style.left=`${U}px`,n.style.maxWidth=`${N}px`}else n.style.left=`${t.offsetLeft}px`,n.style.maxWidth=`${t.offsetWidth}px`;n.style.width="8192px",b&&(n.style.transition="none"),n.offsetWidth,b&&(n.style.transition="",n.style.opacity="1")}else{if(le(["left","maxWidth","width"]),typeof N=="number"&&t.offsetHeight>=N){const U=Math.floor((t.offsetHeight-N)/2)+t.offsetTop;n.style.top=`${U}px`,n.style.maxHeight=`${N}px`}else n.style.top=`${t.offsetTop}px`,n.style.maxHeight=`${t.offsetHeight}px`;n.style.height="8192px",b&&(n.style.transition="none"),n.offsetHeight,b&&(n.style.transition="",n.style.opacity="1")}}}function q(){if(e.type==="card")return;const{value:t}=u;t&&(t.style.opacity="0")}function le(t){const{value:n}=u;if(n)for(const b of t)n.style[b]=""}function ee(){if(e.type==="card")return;const t=S();t?R(t):q()}function he(){var t;const n=(t=_.value)===null||t===void 0?void 0:t.$el;if(!n)return;const b=S();if(!b)return;const{scrollLeft:T,offsetWidth:N}=n,{offsetLeft:D,offsetWidth:U}=b;T>D?n.scrollTo({top:0,left:D,behavior:"smooth"}):D+U>T+N&&n.scrollTo({top:0,left:D+U-N,behavior:"smooth"})}const ie=j(null);let fe=0,X=null;function pe(t){const n=ie.value;if(n){fe=t.getBoundingClientRect().height;const b=`${fe}px`,T=()=>{n.style.height=b,n.style.maxHeight=b};X?(T(),X(),X=null):X=T}}function ze(t){const n=ie.value;if(n){const b=t.getBoundingClientRect().height,T=()=>{document.body.offsetHeight,n.style.maxHeight=`${b}px`,n.style.height=`${Math.max(fe,b)}px`};X?(X(),X=null,T()):X=T}}function Te(){const t=ie.value;if(t){t.style.maxHeight="",t.style.height="";const{paneWrapperStyle:n}=e;if(typeof n=="string")t.style.cssText=n;else if(n){const{maxHeight:b,height:T}=n;b!==void 0&&(t.style.maxHeight=b),T!==void 0&&(t.style.height=T)}}}const ve={value:[]},xe=j("next");function Re(t){const n=x.value;let b="next";for(const T of ve.value){if(T===n)break;if(T===t){b="prev";break}}xe.value=b,ne(t)}function ne(t){const{onActiveNameChange:n,onUpdateValue:b,"onUpdate:value":T}=e;n&&Z(n,t),b&&Z(b,t),T&&Z(T,t),$.value=t}function oe(t){const{onClose:n}=e;n&&Z(n,t)}function ge(){const{value:t}=u;if(!t)return;const n="transition-disabled";t.classList.add(n),ee(),t.classList.remove(n)}const te=j(null);function se({transitionDisabled:t}){const n=p.value;if(!n)return;t&&n.classList.add("transition-disabled");const b=S();b&&te.value&&(te.value.style.width=`${b.offsetWidth}px`,te.value.style.height=`${b.offsetHeight}px`,te.value.style.transform=`translateX(${b.offsetLeft-ga(getComputedStyle(n).paddingLeft)}px)`,t&&te.value.offsetWidth),t&&n.classList.remove("transition-disabled")}ke([x],()=>{e.type==="segment"&&Le(()=>{se({transitionDisabled:!1})})}),wt(()=>{e.type==="segment"&&se({transitionDisabled:!0})});let ye=0;function Ae(t){var n;if(t.contentRect.width===0&&t.contentRect.height===0||ye===t.contentRect.width)return;ye=t.contentRect.width;const{type:b}=e;if((b==="line"||b==="bar")&&ge(),b!=="segment"){const{placement:T}=e;Pe((T==="top"||T==="bottom"?(n=_.value)===null||n===void 0?void 0:n.$el:F.value)||null)}}const Ne=Ke(Ae,64);ke([()=>e.justifyContent,()=>e.size],()=>{Le(()=>{const{type:t}=e;(t==="line"||t==="bar")&&ge()})});const de=j(!1);function Fe(t){var n;const{target:b,contentRect:{width:T,height:N}}=t,D=b.parentElement.parentElement.offsetWidth,U=b.parentElement.parentElement.offsetHeight,{placement:Se}=e;if(!de.value)Se==="top"||Se==="bottom"?D<T&&(de.value=!0):U<N&&(de.value=!0);else{const{value:_e}=I;if(!_e)return;Se==="top"||Se==="bottom"?D-T>_e.$el.offsetWidth&&(de.value=!1):U-N>_e.$el.offsetHeight&&(de.value=!1)}Pe(((n=_.value)===null||n===void 0?void 0:n.$el)||null)}const We=Ke(Fe,64);function je(){const{onAdd:t}=e;t&&t(),Le(()=>{const n=S(),{value:b}=_;!n||!b||b.scrollTo({left:n.offsetLeft,top:0,behavior:"smooth"})})}function Pe(t){if(!t)return;const{placement:n}=e;if(n==="top"||n==="bottom"){const{scrollLeft:b,scrollWidth:T,offsetWidth:N}=t;k.value=b<=0,O.value=b+N>=T}else{const{scrollTop:b,scrollHeight:T,offsetHeight:N}=t;k.value=b<=0,O.value=b+N>=T}}const He=Ke(t=>{Pe(t.target)},64);Sa(Tt,{triggerRef:Q(e,"trigger"),tabStyleRef:Q(e,"tabStyle"),tabClassRef:Q(e,"tabClass"),addTabStyleRef:Q(e,"addTabStyle"),addTabClassRef:Q(e,"addTabClass"),paneClassRef:Q(e,"paneClass"),paneStyleRef:Q(e,"paneStyle"),mergedClsPrefixRef:h,typeRef:Q(e,"type"),closableRef:Q(e,"closable"),valueRef:x,tabChangeIdRef:B,onBeforeLeaveRef:Q(e,"onBeforeLeave"),activateTab:Re,handleClose:oe,handleAdd:je}),pa(()=>{ee(),he()}),va(()=>{const{value:t}=L;if(!t)return;const{value:n}=h,b=`${n}-tabs-nav-scroll-wrapper--shadow-start`,T=`${n}-tabs-nav-scroll-wrapper--shadow-end`;k.value?t.classList.remove(b):t.classList.add(b),O.value?t.classList.remove(T):t.classList.add(T)});const r={syncBarPosition:()=>{ee()}},g=()=>{se({transitionDisabled:!0})},P=G(()=>{const{value:t}=J,{type:n}=e,b={card:"Card",bar:"Bar",line:"Line",segment:"Segment"}[n],T=`${t}${b}`,{self:{barColor:N,closeIconColor:D,closeIconColorHover:U,closeIconColorPressed:Se,tabColor:_e,tabBorderColor:Rt,paneTextColor:Pt,tabFontWeight:_t,tabBorderRadius:Bt,tabFontWeightActive:$t,colorSegment:It,fontWeightStrong:Vt,tabColorSegment:kt,closeSize:Lt,closeIconSize:Mt,closeColorHover:Ot,closeColorPressed:Et,closeBorderRadius:At,[K("panePadding",t)]:Ie,[K("tabPadding",T)]:Nt,[K("tabPaddingVertical",T)]:Ft,[K("tabGap",T)]:Wt,[K("tabGap",`${T}Vertical`)]:jt,[K("tabTextColor",n)]:Ht,[K("tabTextColorActive",n)]:Dt,[K("tabTextColorHover",n)]:Ut,[K("tabTextColorDisabled",n)]:Gt,[K("tabFontSize",t)]:Jt},common:{cubicBezierEaseInOut:Xt}}=z.value;return{"--n-bezier":Xt,"--n-color-segment":It,"--n-bar-color":N,"--n-tab-font-size":Jt,"--n-tab-text-color":Ht,"--n-tab-text-color-active":Dt,"--n-tab-text-color-disabled":Gt,"--n-tab-text-color-hover":Ut,"--n-pane-text-color":Pt,"--n-tab-border-color":Rt,"--n-tab-border-radius":Bt,"--n-close-size":Lt,"--n-close-icon-size":Mt,"--n-close-color-hover":Ot,"--n-close-color-pressed":Et,"--n-close-border-radius":At,"--n-close-icon-color":D,"--n-close-icon-color-hover":U,"--n-close-icon-color-pressed":Se,"--n-tab-color":_e,"--n-tab-font-weight":_t,"--n-tab-font-weight-active":$t,"--n-tab-padding":Nt,"--n-tab-padding-vertical":Ft,"--n-tab-gap":Wt,"--n-tab-gap-vertical":jt,"--n-pane-padding-left":$e(Ie,"left"),"--n-pane-padding-right":$e(Ie,"right"),"--n-pane-padding-top":$e(Ie,"top"),"--n-pane-padding-bottom":$e(Ie,"bottom"),"--n-font-weight-strong":Vt,"--n-tab-color-segment":kt}}),A=i?xt("tabs",G(()=>`${J.value[0]}${e.type[0]}`),P,e):void 0;return Object.assign({mergedClsPrefix:h,mergedValue:x,renderedNames:new Set,segmentCapsuleElRef:te,tabsPaneWrapperRef:ie,tabsElRef:p,barElRef:u,addTabInstRef:I,xScrollInstRef:_,scrollWrapperElRef:L,addTabFixed:de,tabWrapperStyle:a,handleNavResize:Ne,mergedSize:J,handleScroll:He,handleTabsResize:We,cssVars:i?void 0:P,themeClass:A==null?void 0:A.themeClass,animationDirection:xe,renderNameListRef:ve,yScrollElRef:F,handleSegmentResize:g,onAnimationBeforeLeave:pe,onAnimationEnter:ze,onAnimationAfterEnter:Te,onRender:A==null?void 0:A.onRender},r)},render(){const{mergedClsPrefix:e,type:l,placement:s,addTabFixed:d,addable:c,mergedSize:C,renderNameListRef:h,onRender:i,paneWrapperClass:w,paneWrapperStyle:z,$slots:{default:p,prefix:u,suffix:L}}=this;i==null||i();const I=p?De(p()).filter($=>$.type.__TAB_PANE__===!0):[],_=p?De(p()).filter($=>$.type.__TAB__===!0):[],F=!_.length,k=l==="card",O=l==="segment",E=!k&&!O&&this.justifyContent;h.value=[];const J=()=>{const $=f("div",{style:this.tabWrapperStyle,class:`${e}-tabs-wrapper`},E?null:f("div",{class:`${e}-tabs-scroll-padding`,style:s==="top"||s==="bottom"?{width:`${this.tabsPadding}px`}:{height:`${this.tabsPadding}px`}}),F?I.map((x,B)=>(h.value.push(x.props.name),Ye(f(Ee,Object.assign({},x.props,{internalCreatedByPane:!0,internalLeftPadded:B!==0&&(!E||E==="center"||E==="start"||E==="end")}),x.children?{default:x.children.tab}:void 0)))):_.map((x,B)=>(h.value.push(x.props.name),Ye(B!==0&&!E?mt(x):x))),!d&&c&&k?gt(c,(F?I.length:_.length)!==0):null,E?null:f("div",{class:`${e}-tabs-scroll-padding`,style:{width:`${this.tabsPadding}px`}}));return f("div",{ref:"tabsElRef",class:`${e}-tabs-nav-scroll-content`},k&&c?f(Ue,{onResize:this.handleTabsResize},{default:()=>$}):$,k?f("div",{class:`${e}-tabs-pad`}):null,k?null:f("div",{ref:"barElRef",class:`${e}-tabs-bar`}))},H=O?"top":s;return f("div",{class:[`${e}-tabs`,this.themeClass,`${e}-tabs--${l}-type`,`${e}-tabs--${C}-size`,E&&`${e}-tabs--flex`,`${e}-tabs--${H}`],style:this.cssVars},f("div",{class:[`${e}-tabs-nav--${l}-type`,`${e}-tabs-nav--${H}`,`${e}-tabs-nav`]},ae(u,$=>$&&f("div",{class:`${e}-tabs-nav__prefix`},$)),O?f(Ue,{onResize:this.handleSegmentResize},{default:()=>f("div",{class:`${e}-tabs-rail`,ref:"tabsElRef"},f("div",{class:`${e}-tabs-capsule`,ref:"segmentCapsuleElRef"},f("div",{class:`${e}-tabs-wrapper`},f("div",{class:`${e}-tabs-tab`}))),F?I.map(($,x)=>(h.value.push($.props.name),f(Ee,Object.assign({},$.props,{internalCreatedByPane:!0,internalLeftPadded:x!==0}),$.children?{default:$.children.tab}:void 0))):_.map(($,x)=>(h.value.push($.props.name),x===0?$:mt($))))}):f(Ue,{onResize:this.handleNavResize},{default:()=>f("div",{class:`${e}-tabs-nav-scroll-wrapper`,ref:"scrollWrapperElRef"},["top","bottom"].includes(H)?f(Oa,{ref:"xScrollInstRef",onScroll:this.handleScroll},{default:J}):f("div",{class:`${e}-tabs-nav-y-scroll`,onScroll:this.handleScroll,ref:"yScrollElRef"},J()))}),d&&c&&k?gt(c,!0):null,ae(L,$=>$&&f("div",{class:`${e}-tabs-nav__suffix`},$))),F&&(this.animated&&(H==="top"||H==="bottom")?f("div",{ref:"tabsPaneWrapperRef",style:z,class:[`${e}-tabs-pane-wrapper`,w]},vt(I,this.mergedValue,this.renderedNames,this.onAnimationBeforeLeave,this.onAnimationEnter,this.onAnimationAfterEnter,this.animationDirection)):vt(I,this.mergedValue,this.renderedNames)))}});function vt(e,l,s,d,c,C,h){const i=[];return e.forEach(w=>{const{name:z,displayDirective:p,"display-directive":u}=w.props,L=_=>p===_||u===_,I=l===z;if(w.key!==void 0&&(w.key=z),I||L("show")||L("show:lazy")&&s.has(z)){s.has(z)||s.add(z);const _=!L("if");i.push(_?ma(w,[[ya,I]]):w)}}),h?f(ha,{name:`${h}-transition`,onBeforeLeave:d,onEnter:c,onAfterEnter:C},{default:()=>i}):i}function gt(e,l){return f(Ee,{ref:"addTabInstRef",key:"__addable",name:"__addable",internalCreatedByPane:!0,internalAddable:!0,internalLeftPadded:l,disabled:typeof e=="object"&&e.disabled})}function mt(e){const l=xa(e);return l.props?l.props.internalLeftPadded=!0:l.props={internalLeftPadded:!0},l}function Ye(e){return Array.isArray(e.dynamicProps)?e.dynamicProps.includes("internalLeftPadded")||e.dynamicProps.push("internalLeftPadded"):e.dynamicProps=["internalLeftPadded"],e}const Sn={class:"settings-view"},Cn={key:0,class:"settings-main"},wn={key:1,class:"settings-main"},zn={class:"provider-form"},Tn={class:"field"},Rn={class:"provider-form"},Pn={class:"field"},_n={class:"field"},Bn={class:"field"},$n={class:"field"},In={class:"field"},Vn={class:"field"},kn={class:"field"},Ln={key:0,class:"provider-form",style:{"margin-top":"8px"}},Mn={class:"field"},On={class:"provider-form"},En={class:"field"},An={class:"section-label"},Nn={class:"field"},Fn={class:"field"},Wn={class:"field"},jn={class:"provider-form",style:{"margin-top":"12px"}},Hn={class:"field"},Dn={class:"provider-form"},Un={class:"field"},Gn={class:"field"},Jn={class:"inline"},Xn={class:"field-inline"},Kn={class:"actions"},Yn=be({__name:"SettingsView",setup(e){var $,x;const l=Ta(),s=on(),d=j(!0),c=j(!1),C=j(null),h=j("edge_tts"),i=Ra({});let w="";wt(async()=>{try{const[B,a]=await Promise.all([Ca(),wa()]);Object.assign(i,JSON.parse(JSON.stringify(B))),w=JSON.stringify(i),C.value=a}catch{s.error("加载配置失败")}finally{d.value=!1}});const z=G(()=>JSON.stringify(i)!==w),p=(($=i.tts_provider)==null?void 0:$.providers)||[],u=G(()=>p.find(B=>B.name===h.value)||{}),L=G(()=>p.map(B=>({label:B.name,value:B.name}))),I=G(()=>{var S;const B=h.value==="cosyvoice"?"cosyvoice":h.value==="sambert"?"sambert":h.value==="MatchaTTS"?"matcha_tts":"edge_tts",a=((S=C.value)==null?void 0:S.voices[B])||[];return h.value==="MatchaTTS"&&a.length===0?[{label:"0 (默认)",value:"0"}]:a.map(R=>({label:R,value:R}))}),_=((x=i.translation_provider)==null?void 0:x.providers)||[],F=G(()=>_.map(B=>({label:B.name,value:B.name}))),k=G(()=>(i.available_devices||[]).map(a=>({label:a.name,value:a.name}))),O=[{label:"中文",value:"中文"},{label:"英语",value:"英语"},{label:"日语",value:"日语"}];async function E(){c.value=!0;try{const B=JSON.parse(JSON.stringify(i));delete B.available_devices,await $a(B),w=JSON.stringify(i),s.success("已保存")}catch{s.error("保存失败")}finally{c.value=!1}}function J(){Object.assign(i,JSON.parse(w)),s.info("已恢复")}const H=l.beforeEach((B,a,S)=>{a.name==="settings"&&z.value?window.confirm("有未保存的更改，是否放弃？")?S():S(!1):S()});return za(H),(B,a)=>(re(),ce("div",Sn,[d.value?(re(),ce("div",Cn,[...a[16]||(a[16]=[y("p",{class:"muted"},"加载中...",-1)])])):(re(),ce("div",wn,[W(V(Ve),{title:"TTS 引擎",size:"small"},{default:ue(()=>[y("div",zn,[y("label",Tn,[a[17]||(a[17]=y("span",null,"默认引擎",-1)),W(V(Be),{value:i.tts_provider.provider,"onUpdate:value":a[0]||(a[0]=S=>i.tts_provider.provider=S),options:L.value,size:"small",style:{width:"100%"}},null,8,["value","options"])])]),W(V(yn),{value:h.value,"onUpdate:value":a[8]||(a[8]=S=>h.value=S),type:"line",size:"small",style:{"margin-top":"8px"}},{default:ue(()=>[(re(!0),ce(Me,null,ot(V(p),S=>(re(),Pa(V(Ee),{key:S.name,name:S.name,tab:S.name},{default:ue(()=>[y("div",Rn,[y("label",Pn,[a[18]||(a[18]=y("span",null,"默认音色",-1)),W(V(Be),{value:u.value.voice,"onUpdate:value":a[1]||(a[1]=R=>u.value.voice=R),options:I.value,filterable:"",clearable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),h.value==="MatchaTTS"?(re(),ce(Me,{key:0},[y("label",_n,[a[19]||(a[19]=y("span",null,"声学模型",-1)),W(V(Y),{value:u.value.matcha_acoustic_model,"onUpdate:value":a[2]||(a[2]=R=>u.value.matcha_acoustic_model=R),size:"small"},null,8,["value"])]),y("label",Bn,[a[20]||(a[20]=y("span",null,"Vocoder",-1)),W(V(Y),{value:u.value.matcha_vocoder,"onUpdate:value":a[3]||(a[3]=R=>u.value.matcha_vocoder=R),size:"small"},null,8,["value"])]),y("label",$n,[a[21]||(a[21]=y("span",null,"Tokens",-1)),W(V(Y),{value:u.value.matcha_tokens,"onUpdate:value":a[4]||(a[4]=R=>u.value.matcha_tokens=R),size:"small"},null,8,["value"])]),y("label",In,[a[22]||(a[22]=y("span",null,"Lexicon",-1)),W(V(Y),{value:u.value.matcha_lexicon,"onUpdate:value":a[5]||(a[5]=R=>u.value.matcha_lexicon=R),size:"small"},null,8,["value"])]),y("label",Vn,[a[23]||(a[23]=y("span",null,"Data 目录",-1)),W(V(Y),{value:u.value.matcha_data_dir,"onUpdate:value":a[6]||(a[6]=R=>u.value.matcha_data_dir=R),size:"small"},null,8,["value"])]),y("label",kn,[a[24]||(a[24]=y("span",null,"Dict 目录",-1)),W(V(Y),{value:u.value.matcha_dict_dir,"onUpdate:value":a[7]||(a[7]=R=>u.value.matcha_dict_dir=R),size:"small"},null,8,["value"])])],64)):rt("",!0)])]),_:1},8,["name","tab"]))),128))]),_:1},8,["value"]),h.value==="cosyvoice"||h.value==="sambert"?(re(),ce("div",Ln,[y("label",Mn,[a[25]||(a[25]=y("span",null,"阿里 API Key",-1)),W(V(Y),{value:i.ali_api_key,"onUpdate:value":a[9]||(a[9]=S=>i.ali_api_key=S),type:"password","show-password-on":"click",size:"small"},null,8,["value"])])])):rt("",!0)]),_:1}),W(V(Ve),{title:"翻译引擎",size:"small"},{default:ue(()=>[y("div",On,[y("label",En,[a[26]||(a[26]=y("span",null,"默认引擎",-1)),W(V(Be),{value:i.translation_provider.provider,"onUpdate:value":a[10]||(a[10]=S=>i.translation_provider.provider=S),options:F.value,size:"small",style:{width:"100%"}},null,8,["value","options"])])]),(re(!0),ce(Me,null,ot(V(_),(S,R)=>(re(),ce("div",{key:R,class:"provider-form",style:_a({marginTop:R>0?"16px":"8px"})},[y("div",An,Ba(S.name),1),y("label",Nn,[a[27]||(a[27]=y("span",null,"API Key",-1)),W(V(Y),{value:V(_)[R].api_key,"onUpdate:value":q=>V(_)[R].api_key=q,type:"password","show-password-on":"click",size:"small"},null,8,["value","onUpdate:value"])]),y("label",Fn,[a[28]||(a[28]=y("span",null,"API URL",-1)),W(V(Y),{value:V(_)[R].url,"onUpdate:value":q=>V(_)[R].url=q,size:"small"},null,8,["value","onUpdate:value"])]),y("label",Wn,[a[29]||(a[29]=y("span",null,"Model",-1)),W(V(Y),{value:V(_)[R].model,"onUpdate:value":q=>V(_)[R].model=q,size:"small"},null,8,["value","onUpdate:value"])])],4))),128)),y("div",jn,[y("label",Hn,[a[30]||(a[30]=y("span",null,"目标翻译语言",-1)),W(V(Be),{value:i.tLanguage,"onUpdate:value":a[11]||(a[11]=S=>i.tLanguage=S),options:O,size:"small",style:{width:"100%"}},null,8,["value"])])])]),_:1}),W(V(Ve),{title:"语音识别",size:"small"},{default:ue(()=>[...a[31]||(a[31]=[y("div",{class:"placeholder"},[y("span",{class:"placeholder-icon"},"⏳"),y("p",null,"Phase 2 开放")],-1)])]),_:1}),W(V(Ve),{title:"音频 & OSC",size:"small"},{default:ue(()=>[y("div",Dn,[y("label",Un,[a[32]||(a[32]=y("span",null,"播放设备",-1)),W(V(Be),{value:i.device,"onUpdate:value":a[12]||(a[12]=S=>i.device=S),options:k.value,filterable:"",size:"small",style:{width:"100%"}},null,8,["value","options"])]),y("label",Gn,[a[34]||(a[34]=y("span",null,"OSC 地址",-1)),y("div",Jn,[W(V(Y),{value:i.osc_host,"onUpdate:value":a[13]||(a[13]=S=>i.osc_host=S),size:"small",style:{width:"140px"}},null,8,["value"]),a[33]||(a[33]=y("span",{class:"sep"},":",-1)),W(V(vn),{value:i.osc_port,"onUpdate:value":a[14]||(a[14]=S=>i.osc_port=S),min:1,max:65535,size:"small",style:{width:"100px"}},null,8,["value"])])]),y("label",Xn,[a[35]||(a[35]=y("span",null,"OSC 启用",-1)),W(V(La),{value:i.osc_enabled,"onUpdate:value":a[15]||(a[15]=S=>i.osc_enabled=S),size:"small"},null,8,["value"])])])]),_:1}),y("div",Kn,[W(V(st),{onClick:J,disabled:!z.value},{default:ue(()=>[...a[36]||(a[36]=[lt("取消",-1)])]),_:1},8,["disabled"]),W(V(st),{type:"primary",onClick:E,loading:c.value,disabled:!z.value},{default:ue(()=>[...a[37]||(a[37]=[lt(" 保存 ",-1)])]),_:1},8,["loading","disabled"])])]))]))}}),Zn=Ia(Yn,[["__scopeId","data-v-eb53fa18"]]);export{Zn as default};
