<xsl:template match="Report">
    <style>
		 th{
			padding: .3em 0 !important;
		}
    </style>
    <div id="options">
        <form class="form">
        <h1 class="toolbar">
        {{#_}}Select Storage{{/_}}
        </h1>
        <p style="padding:10px;">
            <select size="7" name="Id" style="width:100%;">
                <xsl:for-each select="Storage">
                    <option>
                        <xsl:attribute name="value">
                            <xsl:value-of select="Id" />
                        </xsl:attribute>
                        <xsl:value-of select="Id" />
                        -
                        <xsl:value-of select="Name" />
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
	 	   	 <span style="float:right;" >{{#_}}Storage Stock Report{{/_}} (<xsl:value-of select="../Header/StorageName" />)</span>
	   	 </div>

	   	 <table cellspacing="0" cellpadding="0" class="rep-table alt" >
	   	 	<thead>
	   	 		<tr>
	   	 			<th>{{#_}}Row Index{{/_}}</th>
	   	 			<th>{{#_}}Product Id{{/_}}</th>
	   	 			<th>{{#_}}Product Group{{/_}}</th>
	   	 			<th>{{#_}}Product Name{{/_}}</th>
	   	 			<th>{{#_}}Entrance{{/_}}</th>
	   	 			<th>{{#_}}Egress{{/_}}</th>
                    <th>{{#_}}Remain{{/_}}</th>
	   	 		</tr>
	   	 	</thead>
	   	 	<tbody>
	   	 		<xsl:for-each select="Row" >
		   	 		<tr>
		              <td><xsl:value-of select="position()" /></td>
		              <td><xsl:value-of select="ProductId" /></td>
		              <td class="price" ><xsl:value-of select="CategoryName" /></td>
		              <td class="price" ><xsl:value-of select="ProductName" /></td>
		              <td class="price" ><xsl:value-of select="format-number(Entrance,'###,###')" /></td>
		              <td class="price" ><xsl:value-of select="format-number(Egress,'###,###')" /></td>
		               <td class="price" ><xsl:value-of select="format-number(Current,'###,###')" /></td>
					</tr>
				</xsl:for-each>
	   	 	</tbody>
	   	 	<tfoot>
	   	 		<xsl:variable name="SumCredit" select="sum(../Page/Row/Credit)" />
	   	 		<tr>
					<td colspan="4" style="border:none !important;text-align:left;border-right:none;">
                    {{#_}}Total{{/_}}
                    </td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/Entrance),'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/Egress),'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/Current),'###,###')" /></td>
	          </tr>
	   	 	</tfoot>
	   	 </table>
	   	 <span style="font-weight:bold;background:#e6e6e6;margin:0 auto;display:block;text-align:center;width:10em;padding:.2em .5em">
          <xsl:value-of select="../Header/DateTime" />
       </span>
	   </page>
   </xsl:for-each>
</xsl:template>
