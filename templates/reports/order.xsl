<xsl:template match="Report">
    <style>
		 th{
			padding: .3em 0 !important;
		}
    </style>
   <xsl:for-each select="Page">
	   <page>
	   	 <div class="ReprotHeader">
             <img src="/static/uploads/logo.svg" class="logo"/>
		   	 <h1>{{CompanyName}}</h1>
		   	 <span style="float:left;" >
                 {{#_}}Page{{/_}}
                 <xsl:value-of select="position()" />
                 {{#_}}Of{{/_}}
                 <xsl:value-of select="count(../Page)" /></span>
	 	   	 <span style="float:right;" >{{#_}}Order Report{{/_}}</span>
	   	 </div>
         <table cellspacing="0" cellpadding="0" class="rep-table" >
             <tbody>
                 <tr>
                    <td>{{#_}}Order Id{{/_}}</td>
                    <td><xsl:value-of select="../Header/Id"/></td>
                    <td>{{#_}}Supplier{{/_}}</td>
                    <td><xsl:value-of select="../Header/SupplierName"/></td>
                    <td>{{#_}}User{{/_}}</td>
                    <td><xsl:value-of select="../Header/UserName"/></td>
                 </tr>
                 <tr>
                    <td>{{#_}}Date{{/_}}</td>
                    <td><xsl:value-of select="../Header/Date"/></td>
                    <td>{{#_}}Time{{/_}}</td>
                    <td><xsl:value-of select="../Header/Time"/></td>
                    <td>{{#_}}Storage{{/_}}</td>
                    <td><xsl:value-of select="../Header/Storage" /></td>

                 </tr>
             </tbody>
         </table>
	   	 <table cellspacing="0" cellpadding="0" class="rep-table alt" >
	   	 	<thead>
	   	 		<tr>
	   	 			<th>{{#_}}Row Index{{/_}}</th>
	   	 			<th>{{#_}}Product Id{{/_}}</th>
	   	 			<th>{{#_}}Product Group{{/_}}</th>
	   	 			<th>{{#_}}Product Name{{/_}}</th>
	   	 			<th>{{#_}}Quantity{{/_}}</th>
	   	 			<th>{{#_}}Purchase Price{{/_}}</th>
                    <th>{{#_}}Full Purchase Price{{/_}}</th>
	   	 		</tr>
	   	 	</thead>
	   	 	<tbody>
	   	 		<xsl:for-each select="Row" >
		   	 		<tr>
		              <td><xsl:value-of select="position()" /></td>
		              <td><xsl:value-of select="ProductId" /></td>
		              <td class="price" ><xsl:value-of select="Category" /></td>
		              <td class="price" ><xsl:value-of select="ProductName" /></td>
		              <td class="price" ><xsl:value-of select="format-number(Quantity,'###,###')" /></td>
		              <td class="price" ><xsl:value-of select="format-number(UnitPrice,'###,###')" /></td>
		               <td class="price" ><xsl:value-of select="format-number(FullPrice,'###,###')" /></td>
					</tr>
				</xsl:for-each>
	   	 	</tbody>
	   	 	<tfoot>
	   	 		<xsl:variable name="SumCredit" select="sum(../Page/Row/Credit)" />
	   	 		<tr>
					<td colspan="4" style="border:none !important;text-align:left;border-right:none;">
                    {{#_}}Total{{/_}}
                    </td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/Quantity),'###,###')" /></td>
					<td style="background:#ccc" />
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/FullPrice),'###,###')" /></td>
	          </tr>
	   	 	</tfoot>
	   	 </table>
	   	 <span style="font-weight:bold;background:#e6e6e6;margin:0 auto;display:block;text-align:center;width:10em;padding:.2em .5em">
          <xsl:value-of select="../Header/DateTime" />
       </span>
	   </page>
   </xsl:for-each>
</xsl:template>
