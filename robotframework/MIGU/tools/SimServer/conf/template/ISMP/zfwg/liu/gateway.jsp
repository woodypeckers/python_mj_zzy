<%@page import="test.util.test"%>
<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
<style type="text/css">
	#cetenr{
		width: auto;
		height: auto;
		margin-left: 500px;
	}
</style>
</head>
<body>
	<div id="cetenr">
		<!-- 用户填写支付数据 -->
		
			<h1>第三方支付网关模拟器</h1><span style="font-size: 12px">___支付确认</span>
			<hr/>
			<!-- 接受ismp支付请求的数据 -->
			<input type="hidden" name="callbackUrl" value="<%=request.getParameter("callbackUrl")%>">
			<input type="hidden" name="notifyUrl" value="<%=request.getParameter("notifyUrl")%>">
			<input type="hidden" name="merchantId" value="<%=request.getParameter("merchantId")%>">
			<input type="hidden" name="requestId" value="<%=request.getParameter("requestId")%>">
			<input type="hidden" name="type" value="<%=request.getParameter("type")%>">
			<input type="hidden" name="version" value="<%=request.getParameter("version")%>">
			<input type="hidden" name="hmac" value="<%=request.getParameter("hmac")%>">
			<input type="hidden" name="characterSet"  value="<%=request.getParameter("characterSet")%>"/>
			<input type="hidden" name="channelId" value="<%=request.getParameter("channelId")%>">
			<!--业务参数  -->
			<input type="hidden" name="amount" value="<%=request.getParameter("amount")%>">
			<input type="hidden" name="currency" value="<%=request.getParameter("currency")%>">
			<input type="hidden" name="orderDate" value="<%=request.getParameter("orderDate")%>">
			<input type="hidden" name="merchantOrderId" value="<%=request.getParameter("merchantOrderId")%>">
			<input type="hidden" name="merAcDate" value="<%=request.getParameter("merAcDate")%>">
			<input type="hidden" name="merchantAbbr" value="<%=request.getParameter("merchantAbbr")%>">
			<input type="hidden" name="productDesc" value="<%=request.getParameter("productDesc")%>">
			<input type="hidden" name="productId" value="<%=request.getParameter("productId")%>">
			<input type="hidden" name="productName" value="<%=request.getParameter("productName")%>">
			<input type="hidden" name="productNum" value="<%=request.getParameter("productNum")%>">
			<input type="hidden" name="reserved1" value="<%=request.getParameter("Reserved1")%>">
			<input type="hidden" name="reserved2" value="<%=request.getParameter("Reserved2")%>">
			<input type="hidden" name="showUrl" value="<%=request.getParameter("showUrl")%>">
			<input type="hidden" name="payType" value="<%=request.getParameter("payType")%>">
			<input type="hidden" name="SHRULE" value="<%=request.getParameter("SHRULE")%>">
			<input type="hidden" name="period" value="<%=request.getParameter("period")%>">
			<input type="hidden" name="periodUnit" value="<%=request.getParameter("periodUnit")%>">
			
			<form action="gateway_form.jsp">
			<table>
					<input type="hidden" name="notifyUrl" value="<%=request.getParameter("notifyUrl")%>">
					
					<!-- 支付的url和参数 -->
					<input type="hidden" name="merchantOrderId" value="<%=request.getParameter("merchantOrderId")%>">
					<input type="hidden" name="callbackUrl" value="<%=request.getParameter("callbackUrl")%>">
				<tr>
					<td>商户编号</td>
					<td><input type="text" name="merchantId" value="<%=request.getParameter("channelId")%>"  /></td>
				</tr>
				<tr>
					<td>返回码</td>
					<td><input type="text" name="returnCode"  value="<%=request.getParameter("requestId")%>"  /></td>
				</tr>
				<tr>
					<td>返回码描述信息</td>
					<td><input type="text" name="message"   value="订单支付"  /></td>
				</tr>
				<tr>
					<td>接口类型</td>
					<td><input type="text" name="type"  value="<%=request.getParameter("type")%>" /></td>
				</tr>
				<tr>
					<td>版本号</td>
					<td><input type="text" name="version"   value="<%=request.getParameter("version")%>" /></td>
				</tr>
				<tr>
					<td>支付金额</td>
					<td><input type="text" name="amount"  value="<%=request.getParameter("amount")%>" /></td>
				</tr>
				<tr>
					<td>商户订单号</td>
					<td><input type="text" name="orderId"  value="<%=request.getParameter("merchantOrderId")%>" /></td>
				</tr>
				<tr>
					<td>支付时间</td>
					<td><input type="text" name="payDate"   value="<%=request.getParameter("orderDate")%>" /></td>
				</tr>
				<tr>
					<td>保留字段1</td>
					<td><input type="text" name="reserved1"  value="reserved1"  /></td>
				</tr>
				<tr>
					<td>保留字段2</td>
					<td><input type="text" name="reserved2"   value="reserved2"  /></td>
				</tr>
				<tr>
					<td>支付结果</td>
					<td><input type="text" name="status"   value="SUCCESS"  /></td>
				</tr>
				<tr>
					<td>订单提交日期</td>
					<td><input type="text" name="orderDate"  value="<%=request.getParameter("orderDate")%>"  /></td>
				</tr>
				<tr>
					<td>统一支付平台订单号</td>
					<td><input type="text" name="payNo"  value="<%=request.getParameter("merchantId")%>"  /></td>
				</tr>
				<tr>
					<td>外围支付信息</td>
					<td><input type="text" name="org_code"  value="请求支付"  /></td>
				</tr>
				<tr>
					<td>第三方订单编号</td>
					<td><input type="text" name="organization_payNo"   value="10001"  /></td>
				</tr>
			</table>
			<!-- 改成自己的地址和端口号 -->
			<input type="submit" value="支付响应">
		</form>		
	</div>
</body>
</html>