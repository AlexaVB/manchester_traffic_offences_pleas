Function.prototype.bind||(Function.prototype.bind=function(t){if("function"!=typeof this)throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");var e=Array.prototype.slice.call(arguments,1),i=this,n=function(){},s=function(){return i.apply(this instanceof n?this:t,e.concat(Array.prototype.slice.call(arguments)))};return n.prototype=this.prototype,s.prototype=new n,s}),String.prototype.trim||!function(){var t=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;String.prototype.trim=function(){return this.replace(t,"")}}(),function(){"use strict";var t=this,e=t.jQuery;"undefined"==typeof GOVUK&&(t.GOVUK={});var i=function(t,i){var n;this.selectedClass="selected",this.focusedClass="focused",void 0!==i&&e.each(i,function(t,e){this[t]=e}.bind(this)),"string"==typeof t?(n=e(t),this.selector=t,this.setInitialState(e(this.selector))):(this.$elms=t,this.setInitialState(this.$elms)),this.addEvents()};i.prototype.addEvents=function(){"undefined"!=typeof this.$elms?this.addElementLevelEvents():this.addDocumentLevelEvents()},i.prototype.setInitialState=function(t){t.each(function(t,i){var n=e(i);n.is(":checked")&&this.markSelected(n)}.bind(this))},i.prototype.markFocused=function(t,e){"focused"===e?t.parent("label").addClass(this.focusedClass):t.parent("label").removeClass(this.focusedClass)},i.prototype.markSelected=function(t){var i;"radio"===t.attr("type")?(i=t.attr("name"),e(t[0].form).find('input[name="'+i+'"]').parent("label").removeClass(this.selectedClass),t.parent("label").addClass(this.selectedClass)):t.is(":checked")?t.parent("label").addClass(this.selectedClass):t.parent("label").removeClass(this.selectedClass)},i.prototype.addElementLevelEvents=function(){this.clickHandler=this.getClickHandler(),this.focusHandler=this.getFocusHandler({level:"element"}),this.$elms.on("click",this.clickHandler).on("focus blur",this.focusHandler)},i.prototype.addDocumentLevelEvents=function(){this.clickHandler=this.getClickHandler(),this.focusHandler=this.getFocusHandler({level:"document"}),e(document).on("click",this.selector,this.clickHandler).on("focus blur",this.selector,this.focusHandler)},i.prototype.getClickHandler=function(){return function(t){this.markSelected(e(t.target))}.bind(this)},i.prototype.getFocusHandler=function(t){var i="document"===t.level?"focusin":"focus";return function(t){var n=t.type===i?"focused":"blurred";this.markFocused(e(t.target),n)}.bind(this)},i.prototype.destroy=function(){"undefined"!=typeof this.selector?e(document).off("click",this.selector,this.clickHandler).off("focus blur",this.selector,this.focusHandler):this.$elms.off("click",this.clickHandler).off("focus blur",this.focusHandler)},t.GOVUK.SelectionButtons=i}.call(this),function(){"use strict";window.moj=window.moj||{Modules:{},Events:$({})};var t=function(t,e){return this.init(t,e),this};t.prototype={defaults:{terms:".term",precision:2},init:function(t,e){this.settings=$.extend({},this.defaults,e),this.termSelector=t.data("totalTerms")||this.settings.terms,this.precision=t.data("totalPrecision")||this.settings.precision,this.cacheElements(t),this.bindEvents()},cacheElements:function(t){this.$total=t,this.$terms=$(this.termSelector)},bindEvents:function(){var t=this;this.$terms.on("change.CalculateTotals update.CalculateTotals",function(){t.updateTotal()}),moj.Events.on("render.CalculateTotals",function(){t.updateTotal()})},getNumericValue:function(t){var e=t.text();return t.is(":input")&&(e=t.val()),e=e.replace(/,/g,""),$.isNumeric(e)?parseFloat(e):0},getTotal:function(){var t=this,e=0;return this.$terms.each(function(){e+=t.getNumericValue($(this))}),e},updateTotal:function(){var t=this.getTotal();t=this.formatNumber(t),this.$total.text(t).trigger("update.CalculateTotals")},formatNumber:function(t){var e=t.toFixed(this.precision).toString().split(".");return e[0]=e[0].replace(/\B(?=(\d{3})+(?!\d))/g,","),e.join(".")}},moj.Modules._CalculateTotals=t,moj.Modules.CalculateTotals={init:function(){return $(".js-CalculateTotals").each(function(){$(this).data("CalculateTotals",new t($(this),$(this).data()))})}}}(),function(){"use strict";window.moj=window.moj||{Modules:{},Events:$({})};var t=function(t,e){return this.init(t,e),this};t.prototype={defaults:{},init:function(t,e){this.settings=$.extend({},this.defaults,e),this.cacheElements(t),this.addAriaAttributes(),this.bindEvents()},cacheElements:function(t){this.$conditional=t,this.$inputs=$('[name="'+t.data("conditionalTrigger")+'"]')},bindEvents:function(){var t=this;this.$inputs.on("change.Conditional",function(){t.toggle()}),moj.Events.on("render.Conditional",function(){t.toggle()})},addAriaAttributes:function(){this.$inputs.attr("aria-controls",this.$conditional.attr("id"))},getInputValue:function(t){switch(t.attr("type")){case"radio":return $('[name="'+t.attr("name")+'"]:checked').attr("value");case"checkbox":return t.filter(":checked").val();default:return t.val()||t.find(":selected").attr("value")}},toggle:function(){var t=this.getInputValue(this.$inputs),e=new RegExp(this.$conditional.data("conditionalValue"));t&&t.match(e)?this.$conditional.show().attr("aria-expanded","true").attr("aria-hidden","false"):this.$conditional.hide().attr("aria-expanded","false").attr("aria-hidden","true")}},moj.Modules._Conditional=t,moj.Modules.Conditional={init:function(){return $(".js-Conditional").each(function(){$(this).data("Conditional",new t($(this),$(this).data()))})}}}(),function(){"use strict";window.moj=window.moj||{Modules:{},Events:$({})};var t=function(t,e){return this.init(t,e),this};t.prototype={init:function(t,e){$("<i>").addClass("arrow arrow-closed").text("►").prependTo($(".details-trigger",t)),this.cacheElements(t),this.addAriaAttributes(),this.bindEvents(),this.isOpera="[object Opera]"==Object.prototype.toString.call(window.opera),this.openText=this.$details.data("summary-open"),this.closedText=this.$summaryText.text(),this.updateState()},cacheElements:function(t){this.$details=t,this.$summary=$(".details-trigger",t),this.$summaryText=$(".summary",this.$summary),this.$content=$(".details-content",t),this.$icon=$("i.arrow",this.$summary)},addAriaAttributes:function(){var t=this.$content.attr("id");t||(t="js-details-"+this.$details.index(".js-Details"),this.$content.attr("id",t)),this.$summary.attr({role:"button","aria-controls":t,"aria-expanded":"false"}),this.$content.attr({"aria-hidden":"true"})},bindEvents:function(){var t=this;this.$summary.off("click.details keydown.details").on({"click.details":function(e){e.preventDefault(),t.toggleContent()},"keydown.details":function(e){(32==e.keyCode||13==e.keyCode&&!t.isOpera)&&(e.preventDefault(),t.$summary.click())}})},updateState:function(){this.$details.hasClass("open")?(this.$summary.attr("aria-expanded","true"),this.$content.show().attr("aria-hidden","false"),this.$icon.removeClass("arrow-closed").addClass("arrow-open").text("▼"),this.openText&&this.$summaryText.text(this.openText)):(this.$summary.attr("aria-expanded","false"),this.$content.hide().attr("aria-hidden","true"),this.$icon.removeClass("arrow-open").addClass("arrow-closed").text("►"),this.openText&&this.$summaryText.text(this.closedText))},toggleContent:function(){this.$details.toggleClass("open"),this.updateState()}},moj.Modules._Details=t,moj.Modules.Details={init:function(){return $(".js-Details").each(function(){$(this).data("Details",new t($(this),$(this).data()))})}}}(),function(){"use strict";window.moj=window.moj||{Modules:{},Events:$({})};var t=function(t,e){return this.init(t,e),this};t.prototype={defaults:{eventCategory:"External links",eventAction:document.location.pathname},init:function(t,e){"undefined"!=typeof ga&&(this.settings=$.extend({},this.defaults,e),this.cacheElements(t),this.bindEvents())},cacheElements:function(t){this.$links=t},bindEvents:function(){var t=this;this.$links.on("click",function(e){e.preventDefault(),t.sendGAEvent($(this))})},sendGAEvent:function(t){var e=this,i=t.attr("href"),n=t.attr("target");ga("send","event",e.settings.eventCategory,i,e.settings.eventAction,{hitCallback:e.openLink(i,n)})},openLink:function(t,e){e&&!/^_(self|parent|top)$/i.test(e)?window.open(t,e):window.location.href=t}},moj.Modules._ExternalLinksTracker=t,moj.Modules.ExternalLinksTracker={init:function(){$("a[rel=external]").each(function(){$(this).data("ExternalLinksTracker",new t($(this),$(this).data()))})}}}(),function(){"use strict";window.moj=window.moj||{Modules:{},Events:$({})};var t=function(t){return this.init(t),this};t.prototype={defaults:{message:"You have entered some information"},init:function(t){this.settings=$.extend({},this.defaults,t),this.enable(),this.initMetaRefresh(),this.hashedFields=this.hashFields(),this.bindEvents()},bindEvents:function(){var t=this;$("form").on("submit",function(){t.disable()}),$(window).on("beforeunload",function(){return t.runCheck()})},hashFields:function(){return $("form").serialize()},fieldsHaveChanged:function(){return this.hashFields()!==this.hashedFields},runCheck:function(){var t=this;return this.isEnabled&&this.fieldsHaveChanged()&&this.isMetaRefresh()===!1?t.settings.message:void 0},enable:function(){this.isEnabled=!0},disable:function(){this.isEnabled=!1},isMetaRefresh:function(){if("undefined"!=typeof this.metaRefreshAt){var t=(new Date).getTime();if(t>=this.metaRefreshAt)return!0}return!1},initMetaRefresh:function(){var t=$("head").find("meta[http-equiv=refresh]");if(t.length){var e=parseInt(t.attr("content").match(/^\d*/)[0]),i=(new Date).getTime();this.metaRefreshAt=i+1e3*(e-1)}}},moj.Modules._PromptOnChange=t,moj.Modules.PromptOnChange={init:function(){var e={message:$("[name=promptOnChangeMessage]").val()||"You have entered some information"};return new t(e)}}}(),function(){"use strict";window.moj=window.moj||{Modules:{},Events:$({})};var t=function(t,e){return this.init(t,e),this};t.prototype={defaults:{trigger:"",template:"{value}",defaultsFor:null},init:function(t,e){this.settings=$.extend({},this.defaults,e),this.trigger=t.data("templateTrigger")||this.settings.trigger,this.template=t.data("template")||this.settings.template,this.defaultsFor=t.data("templateDefaultsFor")||this.settings.defaultsFor,t.data("templateDelegate")&&(t=$(t.data("templateDelegate"))),this.originalText=t.eq(0).text(),this.cacheElements(t),this.bindEvents()},cacheElements:function(t){this.$element=t,this.$inputs=$(':radio[name="'+this.trigger+'"]')},bindEvents:function(){var t=this;this.$inputs.on("change.TemplatedElement",function(){t.updateText()}),moj.Events.on("render.TemplatedElement",function(){t.updateText()})},getCurrentValue:function(){var t=this.$inputs.filter(":checked"),e=t.attr("data-template-value")||t.parent("label").text();return e.trim()},formatValue:function(t){return t.toLowerCase()},updateText:function(){this.$element.text(this.getText())},getText:function(){var t=this.originalText,e=this.getCurrentValue();return e&&e!==this.defaultsFor&&(e=this.formatValue(e),t=this.populateTemplate(e)),t},populateTemplate:function(t){return this.template.replace("{value}",t)}},moj.Modules._TemplatedElement=t,moj.Modules.TemplatedElement={init:function(){return $(".js-TemplatedElement").each(function(){$(this).data("TemplatedElement",new t($(this),$(this).data()))})}}}(),$(document).ready(function(){jQuery.fx.off=!0;new GOVUK.SelectionButtons($("label input[type='radio'], label input[type='checkbox']"));$("[name^=nojs]").remove()});
//# sourceMappingURL=../maps/application.js.map