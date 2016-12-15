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
                 {{#_}}Serial{{/_}}:
                 <xsl:value-of select="../Header/Serial" />
             </span>
	 	   	 <span style="float:right;" >{{#_}}Installment Paymnet{{/_}}</span>
	   	 </div>
         <table cellspacing="0" cellpadding="0" class="rep-table" >
             <tbody>
                 <tr>
                    <td>{{#_}}Order Id{{/_}}</td>
                    <td><xsl:value-of select="../Header/SaleId"/></td>
                    <td>{{#_}}Customer{{/_}}</td>
                    <td><xsl:value-of select="../Header/Customer"/></td>
                    <td>{{#_}}Date{{/_}}</td>
                    <td><xsl:value-of select="../Header/Date"/></td>
                 </tr>
                 <tr>
                    <td>{{#_}}Payment{{/_}}</td>
                    <td><xsl:value-of select="format-number(../Header/Amount,'###,###')"/></td>
                    <td>{{#_}}Remain{{/_}}</td>
                     <td><xsl:value-of select="format-number(../Header/Remain,'###,###')"/></td>
                    <td>{{#_}}Date Back{{/_}}</td>
                    <td><xsl:value-of select="../Header/DateBack" /></td>

                 </tr>
             </tbody>
         </table>
	   	 <span style="font-weight:bold;background:#e6e6e6;margin:0 auto;display:block;text-align:center;width:10em;padding:.2em .5em">
          <xsl:value-of select="../Header/DateTime" />
       </span>
	   </page>
   </xsl:for-each>
</xsl:template>
