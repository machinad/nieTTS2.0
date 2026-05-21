import{C as xe,L as a,i as k,q as kr,j as V,ar as bo,ah as De,a0 as _r,W as qe,a8 as O,A as Er,ae as Wr,E as Ze,o as he,x as po,l as _,k as i,m as le,au as Xe,O as go,ab as Dr,s as Y,ac as oe,aa as Ue,S as Hr,F as Ir,V as Ar,ak as eo,as as we,am as Mr,ao as xo,al as oo,an as Ye,a1 as Vr,J as Or,av as lo,aq as mo,at as ro,$ as so,n as K,Z as co,N as uo,d as Gr,b as ho,y as b,K as jr,a5 as Lr,r as yo,M as Je,e as Nr,T as We,f as Co,c as wo,p as fo,a6 as Qe,D as ae}from"./index-CEMDB6DU.js";const He=typeof document<"u"&&typeof window<"u",Kr=xe({name:"Eye",render(){return a("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 512 512"},a("path",{d:"M255.66 112c-77.94 0-157.89 45.11-220.83 135.33a16 16 0 0 0-.27 17.77C82.92 340.8 161.8 400 255.66 400c92.84 0 173.34-59.38 221.79-135.25a16.14 16.14 0 0 0 0-17.47C428.89 172.28 347.8 112 255.66 112z",fill:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"32"}),a("circle",{cx:"256",cy:"256",r:"80",fill:"none",stroke:"currentColor","stroke-miterlimit":"10","stroke-width":"32"}))}}),Ur=xe({name:"EyeOff",render(){return a("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 512 512"},a("path",{d:"M432 448a15.92 15.92 0 0 1-11.31-4.69l-352-352a16 16 0 0 1 22.62-22.62l352 352A16 16 0 0 1 432 448z",fill:"currentColor"}),a("path",{d:"M255.66 384c-41.49 0-81.5-12.28-118.92-36.5c-34.07-22-64.74-53.51-88.7-91v-.08c19.94-28.57 41.78-52.73 65.24-72.21a2 2 0 0 0 .14-2.94L93.5 161.38a2 2 0 0 0-2.71-.12c-24.92 21-48.05 46.76-69.08 76.92a31.92 31.92 0 0 0-.64 35.54c26.41 41.33 60.4 76.14 98.28 100.65C162 402 207.9 416 255.66 416a239.13 239.13 0 0 0 75.8-12.58a2 2 0 0 0 .77-3.31l-21.58-21.58a4 4 0 0 0-3.83-1a204.8 204.8 0 0 1-51.16 6.47z",fill:"currentColor"}),a("path",{d:"M490.84 238.6c-26.46-40.92-60.79-75.68-99.27-100.53C349 110.55 302 96 255.66 96a227.34 227.34 0 0 0-74.89 12.83a2 2 0 0 0-.75 3.31l21.55 21.55a4 4 0 0 0 3.88 1a192.82 192.82 0 0 1 50.21-6.69c40.69 0 80.58 12.43 118.55 37c34.71 22.4 65.74 53.88 89.76 91a.13.13 0 0 1 0 .16a310.72 310.72 0 0 1-64.12 72.73a2 2 0 0 0-.15 2.95l19.9 19.89a2 2 0 0 0 2.7.13a343.49 343.49 0 0 0 68.64-78.48a32.2 32.2 0 0 0-.1-34.78z",fill:"currentColor"}),a("path",{d:"M256 160a95.88 95.88 0 0 0-21.37 2.4a2 2 0 0 0-1 3.38l112.59 112.56a2 2 0 0 0 3.38-1A96 96 0 0 0 256 160z",fill:"currentColor"}),a("path",{d:"M165.78 233.66a2 2 0 0 0-3.38 1a96 96 0 0 0 115 115a2 2 0 0 0 1-3.38z",fill:"currentColor"}))}}),{cubicBezierEaseInOut:ue}=kr;function Qr({duration:e=".2s",delay:h=".1s"}={}){return[k("&.fade-in-width-expand-transition-leave-from, &.fade-in-width-expand-transition-enter-to",{opacity:1}),k("&.fade-in-width-expand-transition-leave-to, &.fade-in-width-expand-transition-enter-from",`
 opacity: 0!important;
 margin-left: 0!important;
 margin-right: 0!important;
 `),k("&.fade-in-width-expand-transition-leave-active",`
 overflow: hidden;
 transition:
 opacity ${e} ${ue},
 max-width ${e} ${ue} ${h},
 margin-left ${e} ${ue} ${h},
 margin-right ${e} ${ue} ${h};
 `),k("&.fade-in-width-expand-transition-enter-active",`
 overflow: hidden;
 transition:
 opacity ${e} ${ue} ${h},
 max-width ${e} ${ue},
 margin-left ${e} ${ue},
 margin-right ${e} ${ue};
 `)]}const qr=V("base-wave",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 border-radius: inherit;
`),Xr=xe({name:"BaseWave",props:{clsPrefix:{type:String,required:!0}},setup(e){bo("-base-wave",qr,De(e,"clsPrefix"));const h=O(null),S=O(!1);let p=null;return _r(()=>{p!==null&&window.clearTimeout(p)}),{active:S,selfRef:h,play(){p!==null&&(window.clearTimeout(p),S.value=!1,p=null),qe(()=>{var C;(C=h.value)===null||C===void 0||C.offsetHeight,S.value=!0,p=window.setTimeout(()=>{S.value=!1,p=null},1e3)})}}},render(){const{clsPrefix:e}=this;return a("div",{ref:"selfRef","aria-hidden":!0,class:[`${e}-base-wave`,this.active&&`${e}-base-wave--active`]})}}),Yr=He&&"chrome"in window;He&&navigator.userAgent.includes("Firefox");const So=He&&navigator.userAgent.includes("Safari")&&!Yr,Jr={paddingTiny:"0 8px",paddingSmall:"0 10px",paddingMedium:"0 12px",paddingLarge:"0 14px",clearSize:"16px"};function Zr(e){const{textColor2:h,textColor3:S,textColorDisabled:p,primaryColor:C,primaryColorHover:w,inputColor:$,inputColorDisabled:n,borderColor:g,warningColor:G,warningColorHover:R,errorColor:f,errorColorHover:x,borderRadius:l,lineHeight:d,fontSizeTiny:m,fontSizeSmall:F,fontSizeMedium:v,fontSizeLarge:U,heightTiny:A,heightSmall:N,heightMedium:c,heightLarge:y,actionColor:L,clearColor:t,clearColorHover:u,clearColorPressed:z,placeholderColor:P,placeholderColorDisabled:I,iconColor:M,iconColorDisabled:ee,iconColorHover:J,iconColorPressed:Z,fontWeight:Q}=e;return Object.assign(Object.assign({},Jr),{fontWeight:Q,countTextColorDisabled:p,countTextColor:S,heightTiny:A,heightSmall:N,heightMedium:c,heightLarge:y,fontSizeTiny:m,fontSizeSmall:F,fontSizeMedium:v,fontSizeLarge:U,lineHeight:d,lineHeightTextarea:d,borderRadius:l,iconSize:"16px",groupLabelColor:L,groupLabelTextColor:h,textColor:h,textColorDisabled:p,textDecorationColor:h,caretColor:C,placeholderColor:P,placeholderColorDisabled:I,color:$,colorDisabled:n,colorFocus:$,groupLabelBorder:`1px solid ${g}`,border:`1px solid ${g}`,borderHover:`1px solid ${w}`,borderDisabled:`1px solid ${g}`,borderFocus:`1px solid ${w}`,boxShadowFocus:`0 0 0 2px ${he(C,{alpha:.2})}`,loadingColor:C,loadingColorWarning:G,borderWarning:`1px solid ${G}`,borderHoverWarning:`1px solid ${R}`,colorFocusWarning:$,borderFocusWarning:`1px solid ${R}`,boxShadowFocusWarning:`0 0 0 2px ${he(G,{alpha:.2})}`,caretColorWarning:G,loadingColorError:f,borderError:`1px solid ${f}`,borderHoverError:`1px solid ${x}`,colorFocusError:$,borderFocusError:`1px solid ${x}`,boxShadowFocusError:`0 0 0 2px ${he(f,{alpha:.2})}`,caretColorError:f,clearColor:t,clearColorHover:u,clearColorPressed:z,iconColor:M,iconColorDisabled:ee,iconColorHover:J,iconColorPressed:Z,suffixTextColor:h})}const et=Er({name:"Input",common:Ze,peers:{Scrollbar:Wr},self:Zr}),$o=po("n-input"),ot=V("input",`
 max-width: 100%;
 cursor: text;
 line-height: 1.5;
 z-index: auto;
 outline: none;
 box-sizing: border-box;
 position: relative;
 display: inline-flex;
 border-radius: var(--n-border-radius);
 background-color: var(--n-color);
 transition: background-color .3s var(--n-bezier);
 font-size: var(--n-font-size);
 font-weight: var(--n-font-weight);
 --n-padding-vertical: calc((var(--n-height) - 1.5 * var(--n-font-size)) / 2);
`,[i("input, textarea",`
 overflow: hidden;
 flex-grow: 1;
 position: relative;
 `),i("input-el, textarea-el, input-mirror, textarea-mirror, separator, placeholder",`
 box-sizing: border-box;
 font-size: inherit;
 line-height: 1.5;
 font-family: inherit;
 border: none;
 outline: none;
 background-color: #0000;
 text-align: inherit;
 transition:
 -webkit-text-fill-color .3s var(--n-bezier),
 caret-color .3s var(--n-bezier),
 color .3s var(--n-bezier),
 text-decoration-color .3s var(--n-bezier);
 `),i("input-el, textarea-el",`
 -webkit-appearance: none;
 scrollbar-width: none;
 width: 100%;
 min-width: 0;
 text-decoration-color: var(--n-text-decoration-color);
 color: var(--n-text-color);
 caret-color: var(--n-caret-color);
 background-color: transparent;
 `,[k("&::-webkit-scrollbar, &::-webkit-scrollbar-track-piece, &::-webkit-scrollbar-thumb",`
 width: 0;
 height: 0;
 display: none;
 `),k("&::placeholder",`
 color: #0000;
 -webkit-text-fill-color: transparent !important;
 `),k("&:-webkit-autofill ~",[i("placeholder","display: none;")])]),_("round",[le("textarea","border-radius: calc(var(--n-height) / 2);")]),i("placeholder",`
 pointer-events: none;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 overflow: hidden;
 color: var(--n-placeholder-color);
 `,[k("span",`
 width: 100%;
 display: inline-block;
 `)]),_("textarea",[i("placeholder","overflow: visible;")]),le("autosize","width: 100%;"),_("autosize",[i("textarea-el, input-el",`
 position: absolute;
 top: 0;
 left: 0;
 height: 100%;
 `)]),V("input-wrapper",`
 overflow: hidden;
 display: inline-flex;
 flex-grow: 1;
 position: relative;
 padding-left: var(--n-padding-left);
 padding-right: var(--n-padding-right);
 `),i("input-mirror",`
 padding: 0;
 height: var(--n-height);
 line-height: var(--n-height);
 overflow: hidden;
 visibility: hidden;
 position: static;
 white-space: pre;
 pointer-events: none;
 `),i("input-el",`
 padding: 0;
 height: var(--n-height);
 line-height: var(--n-height);
 `,[k("&[type=password]::-ms-reveal","display: none;"),k("+",[i("placeholder",`
 display: flex;
 align-items: center; 
 `)])]),le("textarea",[i("placeholder","white-space: nowrap;")]),i("eye",`
 display: flex;
 align-items: center;
 justify-content: center;
 transition: color .3s var(--n-bezier);
 `),_("textarea","width: 100%;",[V("input-word-count",`
 position: absolute;
 right: var(--n-padding-right);
 bottom: var(--n-padding-vertical);
 `),_("resizable",[V("input-wrapper",`
 resize: vertical;
 min-height: var(--n-height);
 `)]),i("textarea-el, textarea-mirror, placeholder",`
 height: 100%;
 padding-left: 0;
 padding-right: 0;
 padding-top: var(--n-padding-vertical);
 padding-bottom: var(--n-padding-vertical);
 word-break: break-word;
 display: inline-block;
 vertical-align: bottom;
 box-sizing: border-box;
 line-height: var(--n-line-height-textarea);
 margin: 0;
 resize: none;
 white-space: pre-wrap;
 scroll-padding-block-end: var(--n-padding-vertical);
 `),i("textarea-mirror",`
 width: 100%;
 pointer-events: none;
 overflow: hidden;
 visibility: hidden;
 position: static;
 white-space: pre-wrap;
 overflow-wrap: break-word;
 `)]),_("pair",[i("input-el, placeholder","text-align: center;"),i("separator",`
 display: flex;
 align-items: center;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 white-space: nowrap;
 `,[V("icon",`
 color: var(--n-icon-color);
 `),V("base-icon",`
 color: var(--n-icon-color);
 `)])]),_("disabled",`
 cursor: not-allowed;
 background-color: var(--n-color-disabled);
 `,[i("border","border: var(--n-border-disabled);"),i("input-el, textarea-el",`
 cursor: not-allowed;
 color: var(--n-text-color-disabled);
 text-decoration-color: var(--n-text-color-disabled);
 `),i("placeholder","color: var(--n-placeholder-color-disabled);"),i("separator","color: var(--n-text-color-disabled);",[V("icon",`
 color: var(--n-icon-color-disabled);
 `),V("base-icon",`
 color: var(--n-icon-color-disabled);
 `)]),V("input-word-count",`
 color: var(--n-count-text-color-disabled);
 `),i("suffix, prefix","color: var(--n-text-color-disabled);",[V("icon",`
 color: var(--n-icon-color-disabled);
 `),V("internal-icon",`
 color: var(--n-icon-color-disabled);
 `)])]),le("disabled",[i("eye",`
 color: var(--n-icon-color);
 cursor: pointer;
 `,[k("&:hover",`
 color: var(--n-icon-color-hover);
 `),k("&:active",`
 color: var(--n-icon-color-pressed);
 `)]),k("&:hover",[i("state-border","border: var(--n-border-hover);")]),_("focus","background-color: var(--n-color-focus);",[i("state-border",`
 border: var(--n-border-focus);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),i("border, state-border",`
 box-sizing: border-box;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 pointer-events: none;
 border-radius: inherit;
 border: var(--n-border);
 transition:
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `),i("state-border",`
 border-color: #0000;
 z-index: 1;
 `),i("prefix","margin-right: 4px;"),i("suffix",`
 margin-left: 4px;
 `),i("suffix, prefix",`
 transition: color .3s var(--n-bezier);
 flex-wrap: nowrap;
 flex-shrink: 0;
 line-height: var(--n-height);
 white-space: nowrap;
 display: inline-flex;
 align-items: center;
 justify-content: center;
 color: var(--n-suffix-text-color);
 `,[V("base-loading",`
 font-size: var(--n-icon-size);
 margin: 0 2px;
 color: var(--n-loading-color);
 `),V("base-clear",`
 font-size: var(--n-icon-size);
 `,[i("placeholder",[V("base-icon",`
 transition: color .3s var(--n-bezier);
 color: var(--n-icon-color);
 font-size: var(--n-icon-size);
 `)])]),k(">",[V("icon",`
 transition: color .3s var(--n-bezier);
 color: var(--n-icon-color);
 font-size: var(--n-icon-size);
 `)]),V("base-icon",`
 font-size: var(--n-icon-size);
 `)]),V("input-word-count",`
 pointer-events: none;
 line-height: 1.5;
 font-size: .85em;
 color: var(--n-count-text-color);
 transition: color .3s var(--n-bezier);
 margin-left: 4px;
 font-variant: tabular-nums;
 `),["warning","error"].map(e=>_(`${e}-status`,[le("disabled",[V("base-loading",`
 color: var(--n-loading-color-${e})
 `),i("input-el, textarea-el",`
 caret-color: var(--n-caret-color-${e});
 `),i("state-border",`
 border: var(--n-border-${e});
 `),k("&:hover",[i("state-border",`
 border: var(--n-border-hover-${e});
 `)]),k("&:focus",`
 background-color: var(--n-color-focus-${e});
 `,[i("state-border",`
 box-shadow: var(--n-box-shadow-focus-${e});
 border: var(--n-border-focus-${e});
 `)]),_("focus",`
 background-color: var(--n-color-focus-${e});
 `,[i("state-border",`
 box-shadow: var(--n-box-shadow-focus-${e});
 border: var(--n-border-focus-${e});
 `)])])]))]),rt=V("input",[_("disabled",[i("input-el, textarea-el",`
 -webkit-text-fill-color: var(--n-text-color-disabled);
 `)])]);function tt(e){let h=0;for(const S of e)h++;return h}function _e(e){return e===""||e==null}function nt(e){const h=O(null);function S(){const{value:w}=e;if(!(w!=null&&w.focus)){C();return}const{selectionStart:$,selectionEnd:n,value:g}=w;if($==null||n==null){C();return}h.value={start:$,end:n,beforeText:g.slice(0,$),afterText:g.slice(n)}}function p(){var w;const{value:$}=h,{value:n}=e;if(!$||!n)return;const{value:g}=n,{start:G,beforeText:R,afterText:f}=$;let x=g.length;if(g.endsWith(f))x=g.length-f.length;else if(g.startsWith(R))x=R.length;else{const l=R[G-1],d=g.indexOf(l,G-1);d!==-1&&(x=d+1)}(w=n.setSelectionRange)===null||w===void 0||w.call(n,x,x)}function C(){h.value=null}return Xe(e,C),{recordCursor:S,restoreCursor:p}}const vo=xe({name:"InputWordCount",setup(e,{slots:h}){const{mergedValueRef:S,maxlengthRef:p,mergedClsPrefixRef:C,countGraphemesRef:w}=go($o),$=Y(()=>{const{value:n}=S;return n===null||Array.isArray(n)?0:(w.value||tt)(n)});return()=>{const{value:n}=p,{value:g}=S;return a("span",{class:`${C.value}-input-word-count`},Dr(h.default,{value:g===null||Array.isArray(g)?"":g},()=>[n===void 0?$.value:`${$.value} / ${n}`]))}}}),it=Object.assign(Object.assign({},we.props),{bordered:{type:Boolean,default:void 0},type:{type:String,default:"text"},placeholder:[Array,String],defaultValue:{type:[String,Array],default:null},value:[String,Array],disabled:{type:Boolean,default:void 0},size:String,rows:{type:[Number,String],default:3},round:Boolean,minlength:[String,Number],maxlength:[String,Number],clearable:Boolean,autosize:{type:[Boolean,Object],default:!1},pair:Boolean,separator:String,readonly:{type:[String,Boolean],default:!1},passivelyActivated:Boolean,showPasswordOn:String,stateful:{type:Boolean,default:!0},autofocus:Boolean,inputProps:Object,resizable:{type:Boolean,default:!0},showCount:Boolean,loading:{type:Boolean,default:void 0},allowInput:Function,renderCount:Function,onMousedown:Function,onKeydown:Function,onKeyup:[Function,Array],onInput:[Function,Array],onFocus:[Function,Array],onBlur:[Function,Array],onClick:[Function,Array],onChange:[Function,Array],onClear:[Function,Array],countGraphemes:Function,status:String,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],textDecoration:[String,Array],attrSize:{type:Number,default:20},onInputBlur:[Function,Array],onInputFocus:[Function,Array],onDeactivate:[Function,Array],onActivate:[Function,Array],onWrapperFocus:[Function,Array],onWrapperBlur:[Function,Array],internalDeactivateOnEnter:Boolean,internalForceFocus:Boolean,internalLoadingBeforeSuffix:{type:Boolean,default:!0},showPasswordToggle:Boolean}),mt=xe({name:"Input",props:it,slots:Object,setup(e){const{mergedClsPrefixRef:h,mergedBorderedRef:S,inlineThemeDisabled:p,mergedRtlRef:C,mergedComponentPropsRef:w}=eo(e),$=we("Input","-input",ot,et,e,h);So&&bo("-input-safari",rt,h);const n=O(null),g=O(null),G=O(null),R=O(null),f=O(null),x=O(null),l=O(null),d=nt(l),m=O(null),{localeRef:F}=Mr("Input"),v=O(e.defaultValue),U=De(e,"value"),A=xo(U,v),N=oo(e,{mergedSize:o=>{var r,s;const{size:W}=e;if(W)return W;const{mergedSize:H}=o||{};if(H!=null&&H.value)return H.value;const B=(s=(r=w==null?void 0:w.value)===null||r===void 0?void 0:r.Input)===null||s===void 0?void 0:s.size;return B||"medium"}}),{mergedSizeRef:c,mergedDisabledRef:y,mergedStatusRef:L}=N,t=O(!1),u=O(!1),z=O(!1),P=O(!1);let I=null;const M=Y(()=>{const{placeholder:o,pair:r}=e;return r?Array.isArray(o)?o:o===void 0?["",""]:[o,o]:o===void 0?[F.value.placeholder]:[o]}),ee=Y(()=>{const{value:o}=z,{value:r}=A,{value:s}=M;return!o&&(_e(r)||Array.isArray(r)&&_e(r[0]))&&s[0]}),J=Y(()=>{const{value:o}=z,{value:r}=A,{value:s}=M;return!o&&s[1]&&(_e(r)||Array.isArray(r)&&_e(r[1]))}),Z=Ye(()=>e.internalForceFocus||t.value),Q=Ye(()=>{if(y.value||e.readonly||!e.clearable||!Z.value&&!u.value)return!1;const{value:o}=A,{value:r}=Z;return e.pair?!!(Array.isArray(o)&&(o[0]||o[1]))&&(u.value||r):!!o&&(u.value||r)}),E=Y(()=>{const{showPasswordOn:o}=e;if(o)return o;if(e.showPasswordToggle)return"click"}),X=O(!1),fe=Y(()=>{const{textDecoration:o}=e;return o?Array.isArray(o)?o.map(r=>({textDecoration:r})):[{textDecoration:o}]:["",""]}),re=O(void 0),te=()=>{var o,r;if(e.type==="textarea"){const{autosize:s}=e;if(s&&(re.value=(r=(o=m.value)===null||o===void 0?void 0:o.$el)===null||r===void 0?void 0:r.offsetWidth),!g.value||typeof s=="boolean")return;const{paddingTop:W,paddingBottom:H,lineHeight:B}=window.getComputedStyle(g.value),ve=Number(W.slice(0,-2)),be=Number(H.slice(0,-2)),pe=Number(B.slice(0,-2)),{value:Pe}=G;if(!Pe)return;if(s.minRows){const Te=Math.max(s.minRows,1),Ke=`${ve+be+pe*Te}px`;Pe.style.minHeight=Ke}if(s.maxRows){const Te=`${ve+be+pe*s.maxRows}px`;Pe.style.maxHeight=Te}}},ne=Y(()=>{const{maxlength:o}=e;return o===void 0?void 0:Number(o)});Vr(()=>{const{value:o}=A;Array.isArray(o)||Ne(o)});const Se=Or().proxy;function se(o,r){const{onUpdateValue:s,"onUpdate:value":W,onInput:H}=e,{nTriggerFormInput:B}=N;s&&K(s,o,r),W&&K(W,o,r),H&&K(H,o,r),v.value=o,B()}function de(o,r){const{onChange:s}=e,{nTriggerFormChange:W}=N;s&&K(s,o,r),v.value=o,W()}function D(o){const{onBlur:r}=e,{nTriggerFormBlur:s}=N;r&&K(r,o),s()}function ie(o){const{onFocus:r}=e,{nTriggerFormFocus:s}=N;r&&K(r,o),s()}function ce(o){const{onClear:r}=e;r&&K(r,o)}function T(o){const{onInputBlur:r}=e;r&&K(r,o)}function $e(o){const{onInputFocus:r}=e;r&&K(r,o)}function ze(){const{onDeactivate:o}=e;o&&K(o)}function Ie(){const{onActivate:o}=e;o&&K(o)}function Ae(o){const{onClick:r}=e;r&&K(r,o)}function Me(o){const{onWrapperFocus:r}=e;r&&K(r,o)}function Ve(o){const{onWrapperBlur:r}=e;r&&K(r,o)}function Oe(){z.value=!0}function Ge(o){z.value=!1,o.target===x.value?me(o,1):me(o,0)}function me(o,r=0,s="input"){const W=o.target.value;if(Ne(W),o instanceof InputEvent&&!o.isComposing&&(z.value=!1),e.type==="textarea"){const{value:B}=m;B&&B.syncUnifiedContainer()}if(I=W,z.value)return;d.recordCursor();const H=je(W);if(H)if(!e.pair)s==="input"?se(W,{source:r}):de(W,{source:r});else{let{value:B}=A;Array.isArray(B)?B=[B[0],B[1]]:B=["",""],B[r]=W,s==="input"?se(B,{source:r}):de(B,{source:r})}Se.$forceUpdate(),H||qe(d.restoreCursor)}function je(o){const{countGraphemes:r,maxlength:s,minlength:W}=e;if(r){let B;if(s!==void 0&&(B===void 0&&(B=r(o)),B>Number(s))||W!==void 0&&(B===void 0&&(B=r(o)),B<Number(s)))return!1}const{allowInput:H}=e;return typeof H=="function"?H(o):!0}function j(o){T(o),o.relatedTarget===n.value&&ze(),o.relatedTarget!==null&&(o.relatedTarget===f.value||o.relatedTarget===x.value||o.relatedTarget===g.value)||(P.value=!1),Fe(o,"blur"),l.value=null}function q(o,r){$e(o),t.value=!0,P.value=!0,Ie(),Fe(o,"focus"),r===0?l.value=f.value:r===1?l.value=x.value:r===2&&(l.value=g.value)}function ye(o){e.passivelyActivated&&(Ve(o),Fe(o,"blur"))}function zo(o){e.passivelyActivated&&(t.value=!0,Me(o),Fe(o,"focus"))}function Fe(o,r){o.relatedTarget!==null&&(o.relatedTarget===f.value||o.relatedTarget===x.value||o.relatedTarget===g.value||o.relatedTarget===n.value)||(r==="focus"?(ie(o),t.value=!0):r==="blur"&&(D(o),t.value=!1))}function Po(o,r){me(o,r,"change")}function To(o){Ae(o)}function Ro(o){ce(o),to()}function to(){e.pair?(se(["",""],{source:"clear"}),de(["",""],{source:"clear"})):(se("",{source:"clear"}),de("",{source:"clear"}))}function Fo(o){const{onMousedown:r}=e;r&&r(o);const{tagName:s}=o.target;if(s!=="INPUT"&&s!=="TEXTAREA"){if(e.resizable){const{value:W}=n;if(W){const{left:H,top:B,width:ve,height:be}=W.getBoundingClientRect(),pe=14;if(H+ve-pe<o.clientX&&o.clientX<H+ve&&B+be-pe<o.clientY&&o.clientY<B+be)return}}o.preventDefault(),t.value||no()}}function Bo(){var o;u.value=!0,e.type==="textarea"&&((o=m.value)===null||o===void 0||o.handleMouseEnterWrapper())}function ko(){var o;u.value=!1,e.type==="textarea"&&((o=m.value)===null||o===void 0||o.handleMouseLeaveWrapper())}function _o(){y.value||E.value==="click"&&(X.value=!X.value)}function Eo(o){if(y.value)return;o.preventDefault();const r=W=>{W.preventDefault(),co("mouseup",document,r)};if(so("mouseup",document,r),E.value!=="mousedown")return;X.value=!0;const s=()=>{X.value=!1,co("mouseup",document,s)};so("mouseup",document,s)}function Wo(o){e.onKeyup&&K(e.onKeyup,o)}function Do(o){switch(e.onKeydown&&K(e.onKeydown,o),o.key){case"Escape":Le();break;case"Enter":Ho(o);break}}function Ho(o){var r,s;if(e.passivelyActivated){const{value:W}=P;if(W){e.internalDeactivateOnEnter&&Le();return}o.preventDefault(),e.type==="textarea"?(r=g.value)===null||r===void 0||r.focus():(s=f.value)===null||s===void 0||s.focus()}}function Le(){e.passivelyActivated&&(P.value=!1,qe(()=>{var o;(o=n.value)===null||o===void 0||o.focus()}))}function no(){var o,r,s;y.value||(e.passivelyActivated?(o=n.value)===null||o===void 0||o.focus():((r=g.value)===null||r===void 0||r.focus(),(s=f.value)===null||s===void 0||s.focus()))}function Io(){var o;!((o=n.value)===null||o===void 0)&&o.contains(document.activeElement)&&document.activeElement.blur()}function Ao(){var o,r;(o=g.value)===null||o===void 0||o.select(),(r=f.value)===null||r===void 0||r.select()}function Mo(){y.value||(g.value?g.value.focus():f.value&&f.value.focus())}function Vo(){const{value:o}=n;o!=null&&o.contains(document.activeElement)&&o!==document.activeElement&&Le()}function Oo(o){if(e.type==="textarea"){const{value:r}=g;r==null||r.scrollTo(o)}else{const{value:r}=f;r==null||r.scrollTo(o)}}function Ne(o){const{type:r,pair:s,autosize:W}=e;if(!s&&W)if(r==="textarea"){const{value:H}=G;H&&(H.textContent=`${o??""}\r
`)}else{const{value:H}=R;H&&(o?H.textContent=o:H.innerHTML="&nbsp;")}}function Go(){te()}const io=O({top:"0"});function jo(o){var r;const{scrollTop:s}=o.target;io.value.top=`${-s}px`,(r=m.value)===null||r===void 0||r.syncUnifiedContainer()}let Be=null;lo(()=>{const{autosize:o,type:r}=e;o&&r==="textarea"?Be=Xe(A,s=>{!Array.isArray(s)&&s!==I&&Ne(s)}):Be==null||Be()});let ke=null;lo(()=>{e.type==="textarea"?ke=Xe(A,o=>{var r;!Array.isArray(o)&&o!==I&&((r=m.value)===null||r===void 0||r.syncUnifiedContainer())}):ke==null||ke()}),Lr($o,{mergedValueRef:A,maxlengthRef:ne,mergedClsPrefixRef:h,countGraphemesRef:De(e,"countGraphemes")});const Lo={wrapperElRef:n,inputElRef:f,textareaElRef:g,isCompositing:z,clear:to,focus:no,blur:Io,select:Ao,deactivate:Vo,activate:Mo,scrollTo:Oo},No=mo("Input",C,h),ao=Y(()=>{const{value:o}=c,{common:{cubicBezierEaseInOut:r},self:{color:s,borderRadius:W,textColor:H,caretColor:B,caretColorError:ve,caretColorWarning:be,textDecorationColor:pe,border:Pe,borderDisabled:Te,borderHover:Ke,borderFocus:Ko,placeholderColor:Uo,placeholderColorDisabled:Qo,lineHeightTextarea:qo,colorDisabled:Xo,colorFocus:Yo,textColorDisabled:Jo,boxShadowFocus:Zo,iconSize:er,colorFocusWarning:or,boxShadowFocusWarning:rr,borderWarning:tr,borderFocusWarning:nr,borderHoverWarning:ir,colorFocusError:ar,boxShadowFocusError:lr,borderError:sr,borderFocusError:dr,borderHoverError:cr,clearSize:ur,clearColor:hr,clearColorHover:fr,clearColorPressed:vr,iconColor:br,iconColorDisabled:pr,suffixTextColor:gr,countTextColor:xr,countTextColorDisabled:mr,iconColorHover:yr,iconColorPressed:Cr,loadingColor:wr,loadingColorError:Sr,loadingColorWarning:$r,fontWeight:zr,[b("padding",o)]:Pr,[b("fontSize",o)]:Tr,[b("height",o)]:Rr}}=$.value,{left:Fr,right:Br}=jr(Pr);return{"--n-bezier":r,"--n-count-text-color":xr,"--n-count-text-color-disabled":mr,"--n-color":s,"--n-font-size":Tr,"--n-font-weight":zr,"--n-border-radius":W,"--n-height":Rr,"--n-padding-left":Fr,"--n-padding-right":Br,"--n-text-color":H,"--n-caret-color":B,"--n-text-decoration-color":pe,"--n-border":Pe,"--n-border-disabled":Te,"--n-border-hover":Ke,"--n-border-focus":Ko,"--n-placeholder-color":Uo,"--n-placeholder-color-disabled":Qo,"--n-icon-size":er,"--n-line-height-textarea":qo,"--n-color-disabled":Xo,"--n-color-focus":Yo,"--n-text-color-disabled":Jo,"--n-box-shadow-focus":Zo,"--n-loading-color":wr,"--n-caret-color-warning":be,"--n-color-focus-warning":or,"--n-box-shadow-focus-warning":rr,"--n-border-warning":tr,"--n-border-focus-warning":nr,"--n-border-hover-warning":ir,"--n-loading-color-warning":$r,"--n-caret-color-error":ve,"--n-color-focus-error":ar,"--n-box-shadow-focus-error":lr,"--n-border-error":sr,"--n-border-focus-error":dr,"--n-border-hover-error":cr,"--n-loading-color-error":Sr,"--n-clear-color":hr,"--n-clear-size":ur,"--n-clear-color-hover":fr,"--n-clear-color-pressed":vr,"--n-icon-color":br,"--n-icon-color-hover":yr,"--n-icon-color-pressed":Cr,"--n-icon-color-disabled":pr,"--n-suffix-text-color":gr}}),Ce=p?ro("input",Y(()=>{const{value:o}=c;return o[0]}),ao,e):void 0;return Object.assign(Object.assign({},Lo),{wrapperElRef:n,inputElRef:f,inputMirrorElRef:R,inputEl2Ref:x,textareaElRef:g,textareaMirrorElRef:G,textareaScrollbarInstRef:m,rtlEnabled:No,uncontrolledValue:v,mergedValue:A,passwordVisible:X,mergedPlaceholder:M,showPlaceholder1:ee,showPlaceholder2:J,mergedFocus:Z,isComposing:z,activated:P,showClearButton:Q,mergedSize:c,mergedDisabled:y,textDecorationStyle:fe,mergedClsPrefix:h,mergedBordered:S,mergedShowPasswordOn:E,placeholderStyle:io,mergedStatus:L,textAreaScrollContainerWidth:re,handleTextAreaScroll:jo,handleCompositionStart:Oe,handleCompositionEnd:Ge,handleInput:me,handleInputBlur:j,handleInputFocus:q,handleWrapperBlur:ye,handleWrapperFocus:zo,handleMouseEnter:Bo,handleMouseLeave:ko,handleMouseDown:Fo,handleChange:Po,handleClick:To,handleClear:Ro,handlePasswordToggleClick:_o,handlePasswordToggleMousedown:Eo,handleWrapperKeydown:Do,handleWrapperKeyup:Wo,handleTextAreaMirrorResize:Go,getTextareaScrollContainer:()=>g.value,mergedTheme:$,cssVars:p?void 0:ao,themeClass:Ce==null?void 0:Ce.themeClass,onRender:Ce==null?void 0:Ce.onRender})},render(){var e,h,S,p,C,w,$;const{mergedClsPrefix:n,mergedStatus:g,themeClass:G,type:R,countGraphemes:f,onRender:x}=this,l=this.$slots;return x==null||x(),a("div",{ref:"wrapperElRef",class:[`${n}-input`,`${n}-input--${this.mergedSize}-size`,G,g&&`${n}-input--${g}-status`,{[`${n}-input--rtl`]:this.rtlEnabled,[`${n}-input--disabled`]:this.mergedDisabled,[`${n}-input--textarea`]:R==="textarea",[`${n}-input--resizable`]:this.resizable&&!this.autosize,[`${n}-input--autosize`]:this.autosize,[`${n}-input--round`]:this.round&&R!=="textarea",[`${n}-input--pair`]:this.pair,[`${n}-input--focus`]:this.mergedFocus,[`${n}-input--stateful`]:this.stateful}],style:this.cssVars,tabindex:!this.mergedDisabled&&this.passivelyActivated&&!this.activated?0:void 0,onFocus:this.handleWrapperFocus,onBlur:this.handleWrapperBlur,onClick:this.handleClick,onMousedown:this.handleMouseDown,onMouseenter:this.handleMouseEnter,onMouseleave:this.handleMouseLeave,onCompositionstart:this.handleCompositionStart,onCompositionend:this.handleCompositionEnd,onKeyup:this.handleWrapperKeyup,onKeydown:this.handleWrapperKeydown},a("div",{class:`${n}-input-wrapper`},oe(l.prefix,d=>d&&a("div",{class:`${n}-input__prefix`},d)),R==="textarea"?a(Hr,{ref:"textareaScrollbarInstRef",class:`${n}-input__textarea`,container:this.getTextareaScrollContainer,theme:(h=(e=this.theme)===null||e===void 0?void 0:e.peers)===null||h===void 0?void 0:h.Scrollbar,themeOverrides:(p=(S=this.themeOverrides)===null||S===void 0?void 0:S.peers)===null||p===void 0?void 0:p.Scrollbar,triggerDisplayManually:!0,useUnifiedContainer:!0,internalHoistYRail:!0},{default:()=>{var d,m;const{textAreaScrollContainerWidth:F}=this,v={width:this.autosize&&F&&`${F}px`};return a(Ir,null,a("textarea",Object.assign({},this.inputProps,{ref:"textareaElRef",class:[`${n}-input__textarea-el`,(d=this.inputProps)===null||d===void 0?void 0:d.class],autofocus:this.autofocus,rows:Number(this.rows),placeholder:this.placeholder,value:this.mergedValue,disabled:this.mergedDisabled,maxlength:f?void 0:this.maxlength,minlength:f?void 0:this.minlength,readonly:this.readonly,tabindex:this.passivelyActivated&&!this.activated?-1:void 0,style:[this.textDecorationStyle[0],(m=this.inputProps)===null||m===void 0?void 0:m.style,v],onBlur:this.handleInputBlur,onFocus:U=>{this.handleInputFocus(U,2)},onInput:this.handleInput,onChange:this.handleChange,onScroll:this.handleTextAreaScroll})),this.showPlaceholder1?a("div",{class:`${n}-input__placeholder`,style:[this.placeholderStyle,v],key:"placeholder"},this.mergedPlaceholder[0]):null,this.autosize?a(Ar,{onResize:this.handleTextAreaMirrorResize},{default:()=>a("div",{ref:"textareaMirrorElRef",class:`${n}-input__textarea-mirror`,key:"mirror"})}):null)}}):a("div",{class:`${n}-input__input`},a("input",Object.assign({type:R==="password"&&this.mergedShowPasswordOn&&this.passwordVisible?"text":R},this.inputProps,{ref:"inputElRef",class:[`${n}-input__input-el`,(C=this.inputProps)===null||C===void 0?void 0:C.class],style:[this.textDecorationStyle[0],(w=this.inputProps)===null||w===void 0?void 0:w.style],tabindex:this.passivelyActivated&&!this.activated?-1:($=this.inputProps)===null||$===void 0?void 0:$.tabindex,placeholder:this.mergedPlaceholder[0],disabled:this.mergedDisabled,maxlength:f?void 0:this.maxlength,minlength:f?void 0:this.minlength,value:Array.isArray(this.mergedValue)?this.mergedValue[0]:this.mergedValue,readonly:this.readonly,autofocus:this.autofocus,size:this.attrSize,onBlur:this.handleInputBlur,onFocus:d=>{this.handleInputFocus(d,0)},onInput:d=>{this.handleInput(d,0)},onChange:d=>{this.handleChange(d,0)}})),this.showPlaceholder1?a("div",{class:`${n}-input__placeholder`},a("span",null,this.mergedPlaceholder[0])):null,this.autosize?a("div",{class:`${n}-input__input-mirror`,key:"mirror",ref:"inputMirrorElRef"}," "):null),!this.pair&&oe(l.suffix,d=>d||this.clearable||this.showCount||this.mergedShowPasswordOn||this.loading!==void 0?a("div",{class:`${n}-input__suffix`},[oe(l["clear-icon-placeholder"],m=>(this.clearable||m)&&a(uo,{clsPrefix:n,show:this.showClearButton,onClear:this.handleClear},{placeholder:()=>m,icon:()=>{var F,v;return(v=(F=this.$slots)["clear-icon"])===null||v===void 0?void 0:v.call(F)}})),this.internalLoadingBeforeSuffix?null:d,this.loading!==void 0?a(Gr,{clsPrefix:n,loading:this.loading,showArrow:!1,showClear:!1,style:this.cssVars}):null,this.internalLoadingBeforeSuffix?d:null,this.showCount&&this.type!=="textarea"?a(vo,null,{default:m=>{var F;const{renderCount:v}=this;return v?v(m):(F=l.count)===null||F===void 0?void 0:F.call(l,m)}}):null,this.mergedShowPasswordOn&&this.type==="password"?a("div",{class:`${n}-input__eye`,onMousedown:this.handlePasswordToggleMousedown,onClick:this.handlePasswordToggleClick},this.passwordVisible?Ue(l["password-visible-icon"],()=>[a(ho,{clsPrefix:n},{default:()=>a(Kr,null)})]):Ue(l["password-invisible-icon"],()=>[a(ho,{clsPrefix:n},{default:()=>a(Ur,null)})])):null]):null)),this.pair?a("span",{class:`${n}-input__separator`},Ue(l.separator,()=>[this.separator])):null,this.pair?a("div",{class:`${n}-input-wrapper`},a("div",{class:`${n}-input__input`},a("input",{ref:"inputEl2Ref",type:this.type,class:`${n}-input__input-el`,tabindex:this.passivelyActivated&&!this.activated?-1:void 0,placeholder:this.mergedPlaceholder[1],disabled:this.mergedDisabled,maxlength:f?void 0:this.maxlength,minlength:f?void 0:this.minlength,value:Array.isArray(this.mergedValue)?this.mergedValue[1]:void 0,readonly:this.readonly,style:this.textDecorationStyle[1],onBlur:this.handleInputBlur,onFocus:d=>{this.handleInputFocus(d,1)},onInput:d=>{this.handleInput(d,1)},onChange:d=>{this.handleChange(d,1)}}),this.showPlaceholder2?a("div",{class:`${n}-input__placeholder`},a("span",null,this.mergedPlaceholder[1])):null),oe(l.suffix,d=>(this.clearable||d)&&a("div",{class:`${n}-input__suffix`},[this.clearable&&a(uo,{clsPrefix:n,show:this.showClearButton,onClear:this.handleClear},{icon:()=>{var m;return(m=l["clear-icon"])===null||m===void 0?void 0:m.call(l)},placeholder:()=>{var m;return(m=l["clear-icon-placeholder"])===null||m===void 0?void 0:m.call(l)}}),d]))):null,this.mergedBordered?a("div",{class:`${n}-input__border`}):null,this.mergedBordered?a("div",{class:`${n}-input__state-border`}):null,this.showCount&&R==="textarea"?a(vo,null,{default:d=>{var m;const{renderCount:F}=this;return F?F(d):(m=l.count)===null||m===void 0?void 0:m.call(l,d)}}):null)}});function ge(e){return yo(e,[255,255,255,.16])}function Ee(e){return yo(e,[0,0,0,.12])}const at=po("n-button-group"),lt={paddingTiny:"0 6px",paddingSmall:"0 10px",paddingMedium:"0 14px",paddingLarge:"0 18px",paddingRoundTiny:"0 10px",paddingRoundSmall:"0 14px",paddingRoundMedium:"0 18px",paddingRoundLarge:"0 22px",iconMarginTiny:"6px",iconMarginSmall:"6px",iconMarginMedium:"6px",iconMarginLarge:"6px",iconSizeTiny:"14px",iconSizeSmall:"18px",iconSizeMedium:"18px",iconSizeLarge:"20px",rippleDuration:".6s"};function st(e){const{heightTiny:h,heightSmall:S,heightMedium:p,heightLarge:C,borderRadius:w,fontSizeTiny:$,fontSizeSmall:n,fontSizeMedium:g,fontSizeLarge:G,opacityDisabled:R,textColor2:f,textColor3:x,primaryColorHover:l,primaryColorPressed:d,borderColor:m,primaryColor:F,baseColor:v,infoColor:U,infoColorHover:A,infoColorPressed:N,successColor:c,successColorHover:y,successColorPressed:L,warningColor:t,warningColorHover:u,warningColorPressed:z,errorColor:P,errorColorHover:I,errorColorPressed:M,fontWeight:ee,buttonColor2:J,buttonColor2Hover:Z,buttonColor2Pressed:Q,fontWeightStrong:E}=e;return Object.assign(Object.assign({},lt),{heightTiny:h,heightSmall:S,heightMedium:p,heightLarge:C,borderRadiusTiny:w,borderRadiusSmall:w,borderRadiusMedium:w,borderRadiusLarge:w,fontSizeTiny:$,fontSizeSmall:n,fontSizeMedium:g,fontSizeLarge:G,opacityDisabled:R,colorOpacitySecondary:"0.16",colorOpacitySecondaryHover:"0.22",colorOpacitySecondaryPressed:"0.28",colorSecondary:J,colorSecondaryHover:Z,colorSecondaryPressed:Q,colorTertiary:J,colorTertiaryHover:Z,colorTertiaryPressed:Q,colorQuaternary:"#0000",colorQuaternaryHover:Z,colorQuaternaryPressed:Q,color:"#0000",colorHover:"#0000",colorPressed:"#0000",colorFocus:"#0000",colorDisabled:"#0000",textColor:f,textColorTertiary:x,textColorHover:l,textColorPressed:d,textColorFocus:l,textColorDisabled:f,textColorText:f,textColorTextHover:l,textColorTextPressed:d,textColorTextFocus:l,textColorTextDisabled:f,textColorGhost:f,textColorGhostHover:l,textColorGhostPressed:d,textColorGhostFocus:l,textColorGhostDisabled:f,border:`1px solid ${m}`,borderHover:`1px solid ${l}`,borderPressed:`1px solid ${d}`,borderFocus:`1px solid ${l}`,borderDisabled:`1px solid ${m}`,rippleColor:F,colorPrimary:F,colorHoverPrimary:l,colorPressedPrimary:d,colorFocusPrimary:l,colorDisabledPrimary:F,textColorPrimary:v,textColorHoverPrimary:v,textColorPressedPrimary:v,textColorFocusPrimary:v,textColorDisabledPrimary:v,textColorTextPrimary:F,textColorTextHoverPrimary:l,textColorTextPressedPrimary:d,textColorTextFocusPrimary:l,textColorTextDisabledPrimary:f,textColorGhostPrimary:F,textColorGhostHoverPrimary:l,textColorGhostPressedPrimary:d,textColorGhostFocusPrimary:l,textColorGhostDisabledPrimary:F,borderPrimary:`1px solid ${F}`,borderHoverPrimary:`1px solid ${l}`,borderPressedPrimary:`1px solid ${d}`,borderFocusPrimary:`1px solid ${l}`,borderDisabledPrimary:`1px solid ${F}`,rippleColorPrimary:F,colorInfo:U,colorHoverInfo:A,colorPressedInfo:N,colorFocusInfo:A,colorDisabledInfo:U,textColorInfo:v,textColorHoverInfo:v,textColorPressedInfo:v,textColorFocusInfo:v,textColorDisabledInfo:v,textColorTextInfo:U,textColorTextHoverInfo:A,textColorTextPressedInfo:N,textColorTextFocusInfo:A,textColorTextDisabledInfo:f,textColorGhostInfo:U,textColorGhostHoverInfo:A,textColorGhostPressedInfo:N,textColorGhostFocusInfo:A,textColorGhostDisabledInfo:U,borderInfo:`1px solid ${U}`,borderHoverInfo:`1px solid ${A}`,borderPressedInfo:`1px solid ${N}`,borderFocusInfo:`1px solid ${A}`,borderDisabledInfo:`1px solid ${U}`,rippleColorInfo:U,colorSuccess:c,colorHoverSuccess:y,colorPressedSuccess:L,colorFocusSuccess:y,colorDisabledSuccess:c,textColorSuccess:v,textColorHoverSuccess:v,textColorPressedSuccess:v,textColorFocusSuccess:v,textColorDisabledSuccess:v,textColorTextSuccess:c,textColorTextHoverSuccess:y,textColorTextPressedSuccess:L,textColorTextFocusSuccess:y,textColorTextDisabledSuccess:f,textColorGhostSuccess:c,textColorGhostHoverSuccess:y,textColorGhostPressedSuccess:L,textColorGhostFocusSuccess:y,textColorGhostDisabledSuccess:c,borderSuccess:`1px solid ${c}`,borderHoverSuccess:`1px solid ${y}`,borderPressedSuccess:`1px solid ${L}`,borderFocusSuccess:`1px solid ${y}`,borderDisabledSuccess:`1px solid ${c}`,rippleColorSuccess:c,colorWarning:t,colorHoverWarning:u,colorPressedWarning:z,colorFocusWarning:u,colorDisabledWarning:t,textColorWarning:v,textColorHoverWarning:v,textColorPressedWarning:v,textColorFocusWarning:v,textColorDisabledWarning:v,textColorTextWarning:t,textColorTextHoverWarning:u,textColorTextPressedWarning:z,textColorTextFocusWarning:u,textColorTextDisabledWarning:f,textColorGhostWarning:t,textColorGhostHoverWarning:u,textColorGhostPressedWarning:z,textColorGhostFocusWarning:u,textColorGhostDisabledWarning:t,borderWarning:`1px solid ${t}`,borderHoverWarning:`1px solid ${u}`,borderPressedWarning:`1px solid ${z}`,borderFocusWarning:`1px solid ${u}`,borderDisabledWarning:`1px solid ${t}`,rippleColorWarning:t,colorError:P,colorHoverError:I,colorPressedError:M,colorFocusError:I,colorDisabledError:P,textColorError:v,textColorHoverError:v,textColorPressedError:v,textColorFocusError:v,textColorDisabledError:v,textColorTextError:P,textColorTextHoverError:I,textColorTextPressedError:M,textColorTextFocusError:I,textColorTextDisabledError:f,textColorGhostError:P,textColorGhostHoverError:I,textColorGhostPressedError:M,textColorGhostFocusError:I,textColorGhostDisabledError:P,borderError:`1px solid ${P}`,borderHoverError:`1px solid ${I}`,borderPressedError:`1px solid ${M}`,borderFocusError:`1px solid ${I}`,borderDisabledError:`1px solid ${P}`,rippleColorError:P,waveOpacity:"0.6",fontWeight:ee,fontWeightStrong:E})}const dt={name:"Button",common:Ze,self:st},ct=k([V("button",`
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
 `,[_("color",[i("border",{borderColor:"var(--n-border-color)"}),_("disabled",[i("border",{borderColor:"var(--n-border-color-disabled)"})]),le("disabled",[k("&:focus",[i("state-border",{borderColor:"var(--n-border-color-focus)"})]),k("&:hover",[i("state-border",{borderColor:"var(--n-border-color-hover)"})]),k("&:active",[i("state-border",{borderColor:"var(--n-border-color-pressed)"})]),_("pressed",[i("state-border",{borderColor:"var(--n-border-color-pressed)"})])])]),_("disabled",{backgroundColor:"var(--n-color-disabled)",color:"var(--n-text-color-disabled)"},[i("border",{border:"var(--n-border-disabled)"})]),le("disabled",[k("&:focus",{backgroundColor:"var(--n-color-focus)",color:"var(--n-text-color-focus)"},[i("state-border",{border:"var(--n-border-focus)"})]),k("&:hover",{backgroundColor:"var(--n-color-hover)",color:"var(--n-text-color-hover)"},[i("state-border",{border:"var(--n-border-hover)"})]),k("&:active",{backgroundColor:"var(--n-color-pressed)",color:"var(--n-text-color-pressed)"},[i("state-border",{border:"var(--n-border-pressed)"})]),_("pressed",{backgroundColor:"var(--n-color-pressed)",color:"var(--n-text-color-pressed)"},[i("state-border",{border:"var(--n-border-pressed)"})])]),_("loading","cursor: wait;"),V("base-wave",`
 pointer-events: none;
 top: 0;
 right: 0;
 bottom: 0;
 left: 0;
 animation-iteration-count: 1;
 animation-duration: var(--n-ripple-duration);
 animation-timing-function: var(--n-bezier-ease-out), var(--n-bezier-ease-out);
 `,[_("active",{zIndex:1,animationName:"button-wave-spread, button-wave-opacity"})]),He&&"MozBoxSizing"in document.createElement("div").style?k("&::moz-focus-inner",{border:0}):null,i("border, state-border",`
 position: absolute;
 left: 0;
 top: 0;
 right: 0;
 bottom: 0;
 border-radius: inherit;
 transition: border-color .3s var(--n-bezier);
 pointer-events: none;
 `),i("border",`
 border: var(--n-border);
 `),i("state-border",`
 border: var(--n-border);
 border-color: #0000;
 z-index: 1;
 `),i("icon",`
 margin: var(--n-icon-margin);
 margin-left: 0;
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 max-width: var(--n-icon-size);
 font-size: var(--n-icon-size);
 position: relative;
 flex-shrink: 0;
 `,[V("icon-slot",`
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 position: absolute;
 left: 0;
 top: 50%;
 transform: translateY(-50%);
 display: flex;
 align-items: center;
 justify-content: center;
 `,[Je({top:"50%",originalTransform:"translateY(-50%)"})]),Qr()]),i("content",`
 display: flex;
 align-items: center;
 flex-wrap: nowrap;
 min-width: 0;
 `,[k("~",[i("icon",{margin:"var(--n-icon-margin)",marginRight:0})])]),_("block",`
 display: flex;
 width: 100%;
 `),_("dashed",[i("border, state-border",{borderStyle:"dashed !important"})]),_("disabled",{cursor:"not-allowed",opacity:"var(--n-opacity-disabled)"})]),k("@keyframes button-wave-spread",{from:{boxShadow:"0 0 0.5px 0 var(--n-ripple-color)"},to:{boxShadow:"0 0 0.5px 4.5px var(--n-ripple-color)"}}),k("@keyframes button-wave-opacity",{from:{opacity:"var(--n-wave-opacity)"},to:{opacity:0}})]),ut=Object.assign(Object.assign({},we.props),{color:String,textColor:String,text:Boolean,block:Boolean,loading:Boolean,disabled:Boolean,circle:Boolean,size:String,ghost:Boolean,round:Boolean,secondary:Boolean,tertiary:Boolean,quaternary:Boolean,strong:Boolean,focusable:{type:Boolean,default:!0},keyboard:{type:Boolean,default:!0},tag:{type:String,default:"button"},type:{type:String,default:"default"},dashed:Boolean,renderIcon:Function,iconPlacement:{type:String,default:"left"},attrType:{type:String,default:"button"},bordered:{type:Boolean,default:!0},onClick:[Function,Array],nativeFocusBehavior:{type:Boolean,default:!So},spinProps:Object}),ht=xe({name:"Button",props:ut,slots:Object,setup(e){const h=O(null),S=O(null),p=O(!1),C=Ye(()=>!e.quaternary&&!e.tertiary&&!e.secondary&&!e.text&&(!e.color||e.ghost||e.dashed)&&e.bordered),w=go(at,{}),{inlineThemeDisabled:$,mergedClsPrefixRef:n,mergedRtlRef:g,mergedComponentPropsRef:G}=eo(e),{mergedSizeRef:R}=oo({},{defaultSize:"medium",mergedSize:c=>{var y,L;const{size:t}=e;if(t)return t;const{size:u}=w;if(u)return u;const{mergedSize:z}=c||{};if(z)return z.value;const P=(L=(y=G==null?void 0:G.value)===null||y===void 0?void 0:y.Button)===null||L===void 0?void 0:L.size;return P||"medium"}}),f=Y(()=>e.focusable&&!e.disabled),x=c=>{var y;f.value||c.preventDefault(),!e.nativeFocusBehavior&&(c.preventDefault(),!e.disabled&&f.value&&((y=h.value)===null||y===void 0||y.focus({preventScroll:!0})))},l=c=>{var y;if(!e.disabled&&!e.loading){const{onClick:L}=e;L&&K(L,c),e.text||(y=S.value)===null||y===void 0||y.play()}},d=c=>{switch(c.key){case"Enter":if(!e.keyboard)return;p.value=!1}},m=c=>{switch(c.key){case"Enter":if(!e.keyboard||e.loading){c.preventDefault();return}p.value=!0}},F=()=>{p.value=!1},v=we("Button","-button",ct,dt,e,n),U=mo("Button",g,n),A=Y(()=>{const c=v.value,{common:{cubicBezierEaseInOut:y,cubicBezierEaseOut:L},self:t}=c,{rippleDuration:u,opacityDisabled:z,fontWeight:P,fontWeightStrong:I}=t,M=R.value,{dashed:ee,type:J,ghost:Z,text:Q,color:E,round:X,circle:fe,textColor:re,secondary:te,tertiary:ne,quaternary:Se,strong:se}=e,de={"--n-font-weight":se?I:P};let D={"--n-color":"initial","--n-color-hover":"initial","--n-color-pressed":"initial","--n-color-focus":"initial","--n-color-disabled":"initial","--n-ripple-color":"initial","--n-text-color":"initial","--n-text-color-hover":"initial","--n-text-color-pressed":"initial","--n-text-color-focus":"initial","--n-text-color-disabled":"initial"};const ie=J==="tertiary",ce=J==="default",T=ie?"default":J;if(Q){const j=re||E;D={"--n-color":"#0000","--n-color-hover":"#0000","--n-color-pressed":"#0000","--n-color-focus":"#0000","--n-color-disabled":"#0000","--n-ripple-color":"#0000","--n-text-color":j||t[b("textColorText",T)],"--n-text-color-hover":j?ge(j):t[b("textColorTextHover",T)],"--n-text-color-pressed":j?Ee(j):t[b("textColorTextPressed",T)],"--n-text-color-focus":j?ge(j):t[b("textColorTextHover",T)],"--n-text-color-disabled":j||t[b("textColorTextDisabled",T)]}}else if(Z||ee){const j=re||E;D={"--n-color":"#0000","--n-color-hover":"#0000","--n-color-pressed":"#0000","--n-color-focus":"#0000","--n-color-disabled":"#0000","--n-ripple-color":E||t[b("rippleColor",T)],"--n-text-color":j||t[b("textColorGhost",T)],"--n-text-color-hover":j?ge(j):t[b("textColorGhostHover",T)],"--n-text-color-pressed":j?Ee(j):t[b("textColorGhostPressed",T)],"--n-text-color-focus":j?ge(j):t[b("textColorGhostHover",T)],"--n-text-color-disabled":j||t[b("textColorGhostDisabled",T)]}}else if(te){const j=ce?t.textColor:ie?t.textColorTertiary:t[b("color",T)],q=E||j,ye=J!=="default"&&J!=="tertiary";D={"--n-color":ye?he(q,{alpha:Number(t.colorOpacitySecondary)}):t.colorSecondary,"--n-color-hover":ye?he(q,{alpha:Number(t.colorOpacitySecondaryHover)}):t.colorSecondaryHover,"--n-color-pressed":ye?he(q,{alpha:Number(t.colorOpacitySecondaryPressed)}):t.colorSecondaryPressed,"--n-color-focus":ye?he(q,{alpha:Number(t.colorOpacitySecondaryHover)}):t.colorSecondaryHover,"--n-color-disabled":t.colorSecondary,"--n-ripple-color":"#0000","--n-text-color":q,"--n-text-color-hover":q,"--n-text-color-pressed":q,"--n-text-color-focus":q,"--n-text-color-disabled":q}}else if(ne||Se){const j=ce?t.textColor:ie?t.textColorTertiary:t[b("color",T)],q=E||j;ne?(D["--n-color"]=t.colorTertiary,D["--n-color-hover"]=t.colorTertiaryHover,D["--n-color-pressed"]=t.colorTertiaryPressed,D["--n-color-focus"]=t.colorSecondaryHover,D["--n-color-disabled"]=t.colorTertiary):(D["--n-color"]=t.colorQuaternary,D["--n-color-hover"]=t.colorQuaternaryHover,D["--n-color-pressed"]=t.colorQuaternaryPressed,D["--n-color-focus"]=t.colorQuaternaryHover,D["--n-color-disabled"]=t.colorQuaternary),D["--n-ripple-color"]="#0000",D["--n-text-color"]=q,D["--n-text-color-hover"]=q,D["--n-text-color-pressed"]=q,D["--n-text-color-focus"]=q,D["--n-text-color-disabled"]=q}else D={"--n-color":E||t[b("color",T)],"--n-color-hover":E?ge(E):t[b("colorHover",T)],"--n-color-pressed":E?Ee(E):t[b("colorPressed",T)],"--n-color-focus":E?ge(E):t[b("colorFocus",T)],"--n-color-disabled":E||t[b("colorDisabled",T)],"--n-ripple-color":E||t[b("rippleColor",T)],"--n-text-color":re||(E?t.textColorPrimary:ie?t.textColorTertiary:t[b("textColor",T)]),"--n-text-color-hover":re||(E?t.textColorHoverPrimary:t[b("textColorHover",T)]),"--n-text-color-pressed":re||(E?t.textColorPressedPrimary:t[b("textColorPressed",T)]),"--n-text-color-focus":re||(E?t.textColorFocusPrimary:t[b("textColorFocus",T)]),"--n-text-color-disabled":re||(E?t.textColorDisabledPrimary:t[b("textColorDisabled",T)])};let $e={"--n-border":"initial","--n-border-hover":"initial","--n-border-pressed":"initial","--n-border-focus":"initial","--n-border-disabled":"initial"};Q?$e={"--n-border":"none","--n-border-hover":"none","--n-border-pressed":"none","--n-border-focus":"none","--n-border-disabled":"none"}:$e={"--n-border":t[b("border",T)],"--n-border-hover":t[b("borderHover",T)],"--n-border-pressed":t[b("borderPressed",T)],"--n-border-focus":t[b("borderFocus",T)],"--n-border-disabled":t[b("borderDisabled",T)]};const{[b("height",M)]:ze,[b("fontSize",M)]:Ie,[b("padding",M)]:Ae,[b("paddingRound",M)]:Me,[b("iconSize",M)]:Ve,[b("borderRadius",M)]:Oe,[b("iconMargin",M)]:Ge,waveOpacity:me}=t,je={"--n-width":fe&&!Q?ze:"initial","--n-height":Q?"initial":ze,"--n-font-size":Ie,"--n-padding":fe||Q?"initial":X?Me:Ae,"--n-icon-size":Ve,"--n-icon-margin":Ge,"--n-border-radius":Q?"initial":fe||X?ze:Oe};return Object.assign(Object.assign(Object.assign(Object.assign({"--n-bezier":y,"--n-bezier-ease-out":L,"--n-ripple-duration":u,"--n-opacity-disabled":z,"--n-wave-opacity":me},de),D),$e),je)}),N=$?ro("button",Y(()=>{let c="";const{dashed:y,type:L,ghost:t,text:u,color:z,round:P,circle:I,textColor:M,secondary:ee,tertiary:J,quaternary:Z,strong:Q}=e;y&&(c+="a"),t&&(c+="b"),u&&(c+="c"),P&&(c+="d"),I&&(c+="e"),ee&&(c+="f"),J&&(c+="g"),Z&&(c+="h"),Q&&(c+="i"),z&&(c+=`j${fo(z)}`),M&&(c+=`k${fo(M)}`);const{value:E}=R;return c+=`l${E[0]}`,c+=`m${L[0]}`,c}),A,e):void 0;return{selfElRef:h,waveElRef:S,mergedClsPrefix:n,mergedFocusable:f,mergedSize:R,showBorder:C,enterPressed:p,rtlEnabled:U,handleMousedown:x,handleKeydown:m,handleBlur:F,handleKeyup:d,handleClick:l,customColorCssVars:Y(()=>{const{color:c}=e;if(!c)return null;const y=ge(c);return{"--n-border-color":c,"--n-border-color-hover":y,"--n-border-color-pressed":Ee(c),"--n-border-color-focus":y,"--n-border-color-disabled":c}}),cssVars:$?void 0:A,themeClass:N==null?void 0:N.themeClass,onRender:N==null?void 0:N.onRender}},render(){const{mergedClsPrefix:e,tag:h,onRender:S}=this;S==null||S();const p=oe(this.$slots.default,C=>C&&a("span",{class:`${e}-button__content`},C));return a(h,{ref:"selfElRef",class:[this.themeClass,`${e}-button`,`${e}-button--${this.type}-type`,`${e}-button--${this.mergedSize}-type`,this.rtlEnabled&&`${e}-button--rtl`,this.disabled&&`${e}-button--disabled`,this.block&&`${e}-button--block`,this.enterPressed&&`${e}-button--pressed`,!this.text&&this.dashed&&`${e}-button--dashed`,this.color&&`${e}-button--color`,this.secondary&&`${e}-button--secondary`,this.loading&&`${e}-button--loading`,this.ghost&&`${e}-button--ghost`],tabindex:this.mergedFocusable?0:-1,type:this.attrType,style:this.cssVars,disabled:this.disabled,onClick:this.handleClick,onBlur:this.handleBlur,onMousedown:this.handleMousedown,onKeyup:this.handleKeyup,onKeydown:this.handleKeydown},this.iconPlacement==="right"&&p,a(Nr,{width:!0},{default:()=>oe(this.$slots.icon,C=>(this.loading||this.renderIcon||C)&&a("span",{class:`${e}-button__icon`,style:{margin:We(this.$slots.default)?"0":""}},a(Co,null,{default:()=>this.loading?a(wo,Object.assign({clsPrefix:e,key:"loading",class:`${e}-icon-slot`,strokeWidth:20},this.spinProps)):a("div",{key:"icon",class:`${e}-icon-slot`,role:"none"},this.renderIcon?this.renderIcon():C)})))}),this.iconPlacement==="left"&&p,this.text?null:a(Xr,{ref:"waveElRef",clsPrefix:e}),this.showBorder?a("div",{"aria-hidden":!0,class:`${e}-button__border`,style:this.customColorCssVars}):null,this.showBorder?a("div",{"aria-hidden":!0,class:`${e}-button__state-border`,style:this.customColorCssVars}):null)}}),yt=ht,ft={buttonHeightSmall:"14px",buttonHeightMedium:"18px",buttonHeightLarge:"22px",buttonWidthSmall:"14px",buttonWidthMedium:"18px",buttonWidthLarge:"22px",buttonWidthPressedSmall:"20px",buttonWidthPressedMedium:"24px",buttonWidthPressedLarge:"28px",railHeightSmall:"18px",railHeightMedium:"22px",railHeightLarge:"26px",railWidthSmall:"32px",railWidthMedium:"40px",railWidthLarge:"48px"};function vt(e){const{primaryColor:h,opacityDisabled:S,borderRadius:p,textColor3:C}=e;return Object.assign(Object.assign({},ft),{iconColor:C,textColor:"white",loadingColor:h,opacityDisabled:S,railColor:"rgba(0, 0, 0, .14)",railColorActive:h,buttonBoxShadow:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",buttonColor:"#FFF",railBorderRadiusSmall:p,railBorderRadiusMedium:p,railBorderRadiusLarge:p,buttonBorderRadiusSmall:p,buttonBorderRadiusMedium:p,buttonBorderRadiusLarge:p,boxShadowFocus:`0 0 0 2px ${he(h,{alpha:.2})}`})}const bt={common:Ze,self:vt},pt=V("switch",`
 height: var(--n-height);
 min-width: var(--n-width);
 vertical-align: middle;
 user-select: none;
 -webkit-user-select: none;
 display: inline-flex;
 outline: none;
 justify-content: center;
 align-items: center;
`,[i("children-placeholder",`
 height: var(--n-rail-height);
 display: flex;
 flex-direction: column;
 overflow: hidden;
 pointer-events: none;
 visibility: hidden;
 `),i("rail-placeholder",`
 display: flex;
 flex-wrap: none;
 `),i("button-placeholder",`
 width: calc(1.75 * var(--n-rail-height));
 height: var(--n-rail-height);
 `),V("base-loading",`
 position: absolute;
 top: 50%;
 left: 50%;
 transform: translateX(-50%) translateY(-50%);
 font-size: calc(var(--n-button-width) - 4px);
 color: var(--n-loading-color);
 transition: color .3s var(--n-bezier);
 `,[Je({left:"50%",top:"50%",originalTransform:"translateX(-50%) translateY(-50%)"})]),i("checked, unchecked",`
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 box-sizing: border-box;
 position: absolute;
 white-space: nowrap;
 top: 0;
 bottom: 0;
 display: flex;
 align-items: center;
 line-height: 1;
 `),i("checked",`
 right: 0;
 padding-right: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),i("unchecked",`
 left: 0;
 justify-content: flex-end;
 padding-left: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),k("&:focus",[i("rail",`
 box-shadow: var(--n-box-shadow-focus);
 `)]),_("round",[i("rail","border-radius: calc(var(--n-rail-height) / 2);",[i("button","border-radius: calc(var(--n-button-height) / 2);")])]),le("disabled",[le("icon",[_("rubber-band",[_("pressed",[i("rail",[i("button","max-width: var(--n-button-width-pressed);")])]),i("rail",[k("&:active",[i("button","max-width: var(--n-button-width-pressed);")])]),_("active",[_("pressed",[i("rail",[i("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])]),i("rail",[k("&:active",[i("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])])])])])]),_("active",[i("rail",[i("button","left: calc(100% - var(--n-button-width) - var(--n-offset))")])]),i("rail",`
 overflow: hidden;
 height: var(--n-rail-height);
 min-width: var(--n-rail-width);
 border-radius: var(--n-rail-border-radius);
 cursor: pointer;
 position: relative;
 transition:
 opacity .3s var(--n-bezier),
 background .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 background-color: var(--n-rail-color);
 `,[i("button-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 font-size: calc(var(--n-button-height) - 4px);
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 display: flex;
 justify-content: center;
 align-items: center;
 line-height: 1;
 `,[Je()]),i("button",`
 align-items: center; 
 top: var(--n-offset);
 left: var(--n-offset);
 height: var(--n-button-height);
 width: var(--n-button-width-pressed);
 max-width: var(--n-button-width);
 border-radius: var(--n-button-border-radius);
 background-color: var(--n-button-color);
 box-shadow: var(--n-button-box-shadow);
 box-sizing: border-box;
 cursor: inherit;
 content: "";
 position: absolute;
 transition:
 background-color .3s var(--n-bezier),
 left .3s var(--n-bezier),
 opacity .3s var(--n-bezier),
 max-width .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 `)]),_("active",[i("rail","background-color: var(--n-rail-color-active);")]),_("loading",[i("rail",`
 cursor: wait;
 `)]),_("disabled",[i("rail",`
 cursor: not-allowed;
 opacity: .5;
 `)])]),gt=Object.assign(Object.assign({},we.props),{size:String,value:{type:[String,Number,Boolean],default:void 0},loading:Boolean,defaultValue:{type:[String,Number,Boolean],default:!1},disabled:{type:Boolean,default:void 0},round:{type:Boolean,default:!0},"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],checkedValue:{type:[String,Number,Boolean],default:!0},uncheckedValue:{type:[String,Number,Boolean],default:!1},railStyle:Function,rubberBand:{type:Boolean,default:!0},spinProps:Object,onChange:[Function,Array]});let Re;const Ct=xe({name:"Switch",props:gt,slots:Object,setup(e){Re===void 0&&(typeof CSS<"u"?typeof CSS.supports<"u"?Re=CSS.supports("width","max(1px)"):Re=!1:Re=!0);const{mergedClsPrefixRef:h,inlineThemeDisabled:S,mergedComponentPropsRef:p}=eo(e),C=we("Switch","-switch",pt,bt,e,h),w=oo(e,{mergedSize(u){var z,P;if(e.size!==void 0)return e.size;if(u)return u.mergedSize.value;const I=(P=(z=p==null?void 0:p.value)===null||z===void 0?void 0:z.Switch)===null||P===void 0?void 0:P.size;return I||"medium"}}),{mergedSizeRef:$,mergedDisabledRef:n}=w,g=O(e.defaultValue),G=De(e,"value"),R=xo(G,g),f=Y(()=>R.value===e.checkedValue),x=O(!1),l=O(!1),d=Y(()=>{const{railStyle:u}=e;if(u)return u({focused:l.value,checked:f.value})});function m(u){const{"onUpdate:value":z,onChange:P,onUpdateValue:I}=e,{nTriggerFormInput:M,nTriggerFormChange:ee}=w;z&&K(z,u),I&&K(I,u),P&&K(P,u),g.value=u,M(),ee()}function F(){const{nTriggerFormFocus:u}=w;u()}function v(){const{nTriggerFormBlur:u}=w;u()}function U(){e.loading||n.value||(R.value!==e.checkedValue?m(e.checkedValue):m(e.uncheckedValue))}function A(){l.value=!0,F()}function N(){l.value=!1,v(),x.value=!1}function c(u){e.loading||n.value||u.key===" "&&(R.value!==e.checkedValue?m(e.checkedValue):m(e.uncheckedValue),x.value=!1)}function y(u){e.loading||n.value||u.key===" "&&(u.preventDefault(),x.value=!0)}const L=Y(()=>{const{value:u}=$,{self:{opacityDisabled:z,railColor:P,railColorActive:I,buttonBoxShadow:M,buttonColor:ee,boxShadowFocus:J,loadingColor:Z,textColor:Q,iconColor:E,[b("buttonHeight",u)]:X,[b("buttonWidth",u)]:fe,[b("buttonWidthPressed",u)]:re,[b("railHeight",u)]:te,[b("railWidth",u)]:ne,[b("railBorderRadius",u)]:Se,[b("buttonBorderRadius",u)]:se},common:{cubicBezierEaseInOut:de}}=C.value;let D,ie,ce;return Re?(D=`calc((${te} - ${X}) / 2)`,ie=`max(${te}, ${X})`,ce=`max(${ne}, calc(${ne} + ${X} - ${te}))`):(D=Qe((ae(te)-ae(X))/2),ie=Qe(Math.max(ae(te),ae(X))),ce=ae(te)>ae(X)?ne:Qe(ae(ne)+ae(X)-ae(te))),{"--n-bezier":de,"--n-button-border-radius":se,"--n-button-box-shadow":M,"--n-button-color":ee,"--n-button-width":fe,"--n-button-width-pressed":re,"--n-button-height":X,"--n-height":ie,"--n-offset":D,"--n-opacity-disabled":z,"--n-rail-border-radius":Se,"--n-rail-color":P,"--n-rail-color-active":I,"--n-rail-height":te,"--n-rail-width":ne,"--n-width":ce,"--n-box-shadow-focus":J,"--n-loading-color":Z,"--n-text-color":Q,"--n-icon-color":E}}),t=S?ro("switch",Y(()=>$.value[0]),L,e):void 0;return{handleClick:U,handleBlur:N,handleFocus:A,handleKeyup:c,handleKeydown:y,mergedRailStyle:d,pressed:x,mergedClsPrefix:h,mergedValue:R,checked:f,mergedDisabled:n,cssVars:S?void 0:L,themeClass:t==null?void 0:t.themeClass,onRender:t==null?void 0:t.onRender}},render(){const{mergedClsPrefix:e,mergedDisabled:h,checked:S,mergedRailStyle:p,onRender:C,$slots:w}=this;C==null||C();const{checked:$,unchecked:n,icon:g,"checked-icon":G,"unchecked-icon":R}=w,f=!(We(g)&&We(G)&&We(R));return a("div",{role:"switch","aria-checked":S,class:[`${e}-switch`,this.themeClass,f&&`${e}-switch--icon`,S&&`${e}-switch--active`,h&&`${e}-switch--disabled`,this.round&&`${e}-switch--round`,this.loading&&`${e}-switch--loading`,this.pressed&&`${e}-switch--pressed`,this.rubberBand&&`${e}-switch--rubber-band`],tabindex:this.mergedDisabled?void 0:0,style:this.cssVars,onClick:this.handleClick,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeyup:this.handleKeyup,onKeydown:this.handleKeydown},a("div",{class:`${e}-switch__rail`,"aria-hidden":"true",style:p},oe($,x=>oe(n,l=>x||l?a("div",{"aria-hidden":!0,class:`${e}-switch__children-placeholder`},a("div",{class:`${e}-switch__rail-placeholder`},a("div",{class:`${e}-switch__button-placeholder`}),x),a("div",{class:`${e}-switch__rail-placeholder`},a("div",{class:`${e}-switch__button-placeholder`}),l)):null)),a("div",{class:`${e}-switch__button`},oe(g,x=>oe(G,l=>oe(R,d=>a(Co,null,{default:()=>this.loading?a(wo,Object.assign({key:"loading",clsPrefix:e,strokeWidth:20},this.spinProps)):this.checked&&(l||x)?a("div",{class:`${e}-switch__button-icon`,key:l?"checked-icon":"icon"},l||x):!this.checked&&(d||x)?a("div",{class:`${e}-switch__button-icon`,key:d?"unchecked-icon":"icon"},d||x):null})))),oe($,x=>x&&a("div",{key:"checked",class:`${e}-switch__checked`},x)),oe(n,x=>x&&a("div",{key:"unchecked",class:`${e}-switch__unchecked`},x)))))}});export{ht as B,mt as N,yt as X,Ct as a,dt as b,et as i};
