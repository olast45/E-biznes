package models

case class Cart(id: Long, products: scala.collection.mutable.ListBuffer[Product], var productId: Long = 0)