<xsl:template match="Report">
    <style>
		 th{
			padding: .3em 0 !important;
		}
        td.center,.footsum{text-align:center;}
    </style>
    <div id="options">
        <form class="form">
        <h1 class="toolbar">
        {{#_}}Sale List Report{{/_}}
        </h1>
        <p style="padding:10px;">
            <select size="7" name="User" style="width:100%;">
                <xsl:for-each select="User">
                    <option>
                        <xsl:attribute name="value">
                            <xsl:value-of select="Id" />
                        </xsl:attribute>
                        <xsl:value-of select="Id" />
                        -
                        <xsl:value-of select="UserName" />
                    </option>
                </xsl:for-each>
            </select>
            <button type="button" onclick="CloseDialog()" class="btn">{{#_}}Cancel{{/_}}</button>

            <button type="submit" class="btn" >{{#_}}Select{{/_}}</button>
        </p>
        </form>
    </div>
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
	 	   	 <span style="float:right;" >{{#_}}Sale List Report{{/_}} (<xsl:value-of select="../Header/UserName" />)</span>
	   	 </div>

	   	 <table cellspacing="0" cellpadding="0" class="rep-table alt" >
	   	 	<thead>
	   	 		<tr>
	   	 			<th>{{#_}}Row Index{{/_}}</th>
	   	 			<th>{{#_}}Sale Id{{/_}}</th>
	   	 			<th>{{#_}}Time{{/_}}</th>
	   	 			<th>{{#_}}Customer Name{{/_}}</th>
	   	 			<th>{{#_}}Full Sale Price{{/_}}</th>
	   	 			<th>{{#_}}Prepaid{{/_}}</th>
                    <th>{{#_}}Remain{{/_}}</th>
	   	 		</tr>
	   	 	</thead>
	   	 	<tbody>
	   	 		<xsl:for-each select="Row" >
		   	 		<tr>
		              <td><xsl:value-of select="position()" /></td>
		              <td class="center">
                          <a target="_blank">
                              <xsl:attribute name="href">
                                  /report/sale?Id=<xsl:value-of select="Id"/>
                              </xsl:attribute>
                              <xsl:value-of select="Id" />
                          </a>

                      </td>
		              <td class="center" ><xsl:value-of select="Time" /></td>
		              <td class="center" ><xsl:value-of select="Customer" /></td>
		              <td class="price center" ><xsl:value-of select="format-number(FullSale,'###,###')" /></td>
		              <td class="price center" ><xsl:value-of select="format-number(Prepaid,'###,###')" /></td>
		               <td class="price center" ><xsl:value-of select="format-number(Remain,'###,###')" /></td>
					</tr>
				</xsl:for-each>
	   	 	</tbody>
	   	 	<tfoot>
	   	 		<xsl:variable name="SumCredit" select="sum(../Page/Row/Credit)" />
	   	 		<tr>
					<td colspan="4" style="border:none !important;text-align:left;border-right:none;">
                    {{#_}}Total{{/_}}
                    </td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/FullSale),'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/Prepaid),'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/Remain),'###,###')" /></td>
	          </tr>
	   	 	</tfoot>
	   	 </table>
	   	 <span style="font-weight:bold;background:#e6e6e6;margin:0 auto;display:block;text-align:center;width:10em;padding:.2em .5em">
          <xsl:value-of select="../Header/DateTime" />
       </span>
	   </page>
   </xsl:for-each>
</xsl:template>
