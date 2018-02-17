<xsl:template match="Report">
   <style>
	 .ReprotHeader{
        text-align:center;
        padding:4em 1.2em 1em 1.2em;
      }
      h1{font-size:1.4em;}
      .ledger {
        width:40em;
        margin:1em;
      }
      .ledger td,.ledger th{
        border:solid thin black;
        border-bottom:none;
        border-left:none;
        padding:.2em .5em;
        vertical-align:middle;
       }
      .ledger tr td:last-child ,
      .ledger tr th:last-child{
        border-left:solid thin black;
       }
      .ledger tr:last-child td{
        border-bottom:solid thin black;
       }
      .ledger thead td,
      .ledger thead th{
        background:#7cf;
      }
   </style>
   <xsl:for-each select="Page">
	   <page>
	   	 <div class="ReprotHeader">
		   	 <h1></h1>
		   	 <span style="float:left;" >صفحه <xsl:value-of select="position()" /> از <xsl:value-of select="count(../Page)" /></span>
	 	   	 <span style="float:right;" >تراز کل</span>
	   	 </div>
	   	 <table cellspacing="0" cellpadding="0" class="ledger" >
	   	 	<thead>
	   	 		<tr>
	   	 			<th>کد </th>
	   	 			<th>شرح</th>
	   	 			<th>بدهکار</th>
	   	 			<th>بستانکار</th>
	   	 			<th>مانده بدهکار</th>
	   	 			<th>مانده بستانکار</th>
	   	 		</tr>
	   	 	</thead>
	   	 	<tbody>
	   	 		<xsl:for-each select="Row" >
		   	 		<tr>
		              <td><xsl:value-of select="position()" /></td>
		              <td><xsl:value-of select="Title" /></td>
		              <td class="price" ><xsl:value-of select="format-number(Debit,'###,###')" /></td>
		              <td class="price" ><xsl:value-of select="format-number(Credit,'###,###')" /></td>
		              <td class="price" ><xsl:value-of select="format-number(RemindDebit,'###,###')" /></td>
		              <td class="price" ><xsl:value-of select="format-number(RemindCredit,'###,###')" /></td>
					</tr>
				</xsl:for-each>
	   	 	</tbody>
	   	 	<tfoot>
	   	 		<tr>
	   	 			<td colspan="2" style="text-align:left;border-right:none;" >جمع صفحه	</td>
	   	 			<td class="footsum" ><xsl:value-of select="format-number(sum(Row/Debit),'###,###')" /></td>
	   	 			<td class="footsum" ><xsl:value-of select="format-number(sum(Row/Credit),'###,###')" /></td>
		 			<td class="footsum" ><xsl:value-of select="format-number(sum(Row/RemindDebit),'###,###')" /></td>
		 			<td class="footsum" ><xsl:value-of select="format-number(sum(Row/RemindCredit),'###,###')" /></td>
	   	 		</tr>
	   	 		<xsl:variable name="SumDebit" select="sum(../Page/Row/Debit)" />
	   	 		<xsl:variable name="SumCredit" select="sum(../Page/Row/Credit)" />
	   	 		<tr>
					<td colspan="2" style="border:none !important;text-align:left;border-right:none;" >جمع کل</td>
					<td class="footsum" ><xsl:value-of  select="format-number($SumDebit,'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number($SumCredit,'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/RemindDebit),'###,###')" /></td>
					<td class="footsum" ><xsl:value-of select="format-number(sum(../Page/Row/RemindCredit),'###,###')" /></td>
	          </tr>
	   	 	</tfoot>
	   	 </table>
	   	 <span style="font-weight:bold;background:#e6e6e6;margin:0 auto;display:block;width:12em;padding:.2em .5em">
          <xsl:value-of select="../Header/DateTime" />
       </span>
	   </page>
   </xsl:for-each>
</xsl:template>
