# parser-stage 语法规范（同 step6）


<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>
<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<span class="SpecRuleStart">block_item</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">declaration</span>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span>

<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'if'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span> <span class="SpecOperator">(</span><span class="SpecToken">'else'</span> <span class="SpecRule">statement</span><span class="SpecOperator">)?</span>

<span class="SpecRuleStart">declaration</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>

<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">assignment</span>

<span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span>
<span class="SpecRuleStart">conditional</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_or</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'?'</span> <span class="SpecRule">expression</span> <span class="SpecToken">':'</span> <span class="SpecRule">conditional</span>
<span class="SpecRuleStart">logical_or</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_and</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'||'</span> <span class="SpecRule">logical_and</span>

<span class="SpecRuleStart">logical_and</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">equality</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_and</span> <span class="SpecToken">'&amp;&amp;'</span> <span class="SpecRule">equality</span>

<span class="SpecRuleStart">equality</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">relational</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">equality</span> <span class="SpecOperator">(</span><span class="SpecToken">'=='</span><span class="SpecOperator">|</span><span class="SpecToken">'!='</span><span class="SpecOperator">)</span> <span class="SpecRule">relational</span>

<span class="SpecRuleStart">relational</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">additive</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">relational</span> <span class="SpecOperator">(</span><span class="SpecToken">'&lt;'</span><span class="SpecOperator">|</span><span class="SpecToken">'&gt;'</span><span class="SpecOperator">|</span><span class="SpecToken">'&lt;='</span><span class="SpecOperator">|</span><span class="SpecToken">'&gt;='</span><span class="SpecOperator">)</span> <span class="SpecRule">additive</span>

<span class="SpecRuleStart">additive</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">multiplicative</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">additive</span> <span class="SpecOperator">(</span><span class="SpecToken">'+'</span><span class="SpecOperator">|</span><span class="SpecToken">'-'</span><span class="SpecOperator">)</span> <span class="SpecRule">multiplicative</span>

<span class="SpecRuleStart">multiplicative</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">multiplicative</span> <span class="SpecOperator">(</span><span class="SpecToken">'*'</span><span class="SpecOperator">|</span><span class="SpecToken">'/'</span><span class="SpecOperator">|</span><span class="SpecToken">'%'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">primary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span>
</pre>


