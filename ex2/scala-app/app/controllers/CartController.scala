package controllers

import javax.inject._
import play.api._
import play.api.libs.json._
import play.api.mvc._

import models.Cart
import models.Product

@Singleton
class CartController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {

    var carts = scala.collection.mutable.ListBuffer.empty[Cart]
    var currentId = 0 // Autoincrementing id

    def showAll() = Action { implicit request: Request[AnyContent] => 

        if (carts.isEmpty) {
            NotFound("There are no carts to be displayed!")

        } else {

            val cartsJS: JsArray = JsArray(
            carts.map(cart => Json.obj(
                "id" -> cart.id,
                "products" -> JsArray(cart.products.map(product => Json.obj(
                    "id" -> product.id,
                    "name" -> product.name,
                    "price" -> product.price
                )))
            ))
            )

            Ok(cartsJS)

        }
    }

    def showById(cartId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCart = carts.find(_.id == cartId)

        foundCart match {
            case Some(cart) => Ok(Json.obj(
                "id" -> cart.id,
                "products" -> JsArray(cart.products.map(product => Json.obj(
                    "id" -> product.id,
                    "name" -> product.name,
                    "price" -> product.price
                )))

            ))
            case None => NotFound(s"Cart with id=$cartId not found!")
        }
    }

    def showAllProducts(cartId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCart = carts.find(_.id == cartId)

        foundCart match {
            case Some(cart) =>
            val productsJS: JsArray = JsArray(
                cart.products.map(product => Json.obj(
                "id" -> product.id,
                "name" -> product.name,
                "price" -> product.price
                ))
            )

            Ok(productsJS)

            case None => NotFound(s"Cart with id=$cartId not found!")
        }
    }


    def deleteCart(cartId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCart = carts.find(_.id == cartId)

        foundCart match {
            case Some(cart) => 
                carts -= cart
                Ok(s"Cart with id=$cartId removed")

            case None => NotFound(s"Cart with id=$cartId not found!")
        }
    }

    def deleteAllCarts() = Action { implicit request: Request[AnyContent] =>

        if (carts.isEmpty) {
            NotFound("There are no carts to be deleted!")

        } else {

            carts.clear()

            Ok("All carts were deleted!")
        }
  
    }

    def deleteAllProductsFromCart(cartId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCart = carts.find(_.id == cartId)

        foundCart match {
            case Some(cart) =>
                cart.products.clear()
                Ok(s"Products from cart with id=$cartId removed")

            case None => NotFound(s"Cart with id=$cartId not found!")
        }
  
    }

    def deleteProductFromCart(cartId: Long, productId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundCart = carts.find(_.id == cartId)

        foundCart match {
            case Some(cart) =>
                cart.products.find(_.id == productId) match {
                    case Some(product) =>

                        cart.products -= product
                        Ok(s"Product with id=$productId from cart with id=$cartId removed")

                    case None => NotFound(s"Product with id=$productId not found!")
                }

            case None => NotFound(s"Cart with id=$cartId not found!")
        }
  
    }

    def updateProductInCart(cartId: Long, productId: Long) = Action { implicit request: Request[AnyContent] =>

        request.body.asJson match {
            case Some(body) =>
                val nameOpt = (body \ "name").asOpt[String]
                val priceOpt = (body \ "price").asOpt[Double]

                // Find the cart by ID
                carts.find(_.id == cartId) match {
                    case Some(cart) =>

                        // Find the product inside the cart
                        val foundProductIndex = cart.products.indexWhere(_.id == productId)
                        
                        foundProductIndex match {
                            case index if index >= 0 =>
                                val product = cart.products(index)
                                val updatedProduct = product.copy(
                                    name = nameOpt.getOrElse(product.name),
                                    price = priceOpt.getOrElse(product.price)
                                )

                                cart.products.update(index, updatedProduct)

                                Ok(s"Product with id=$productId updated in Cart id=$cartId!")

                            case _ => NotFound(s"Product with id=$productId not found in Cart id=$cartId!")
                        }

                    case None => NotFound(s"Cart with id=$cartId not found!")
                }

            case None => BadRequest("Request doesn't have a valid JSON body!")
        }
    }


    def createCart() = Action { implicit request: Request[AnyContent] =>

        currentId += 1
        val newCart = Cart(currentId, scala.collection.mutable.ListBuffer.empty[Product])
        carts += newCart

        Ok("New cart was created!")
    }

    def addProductToCart(cartId: Long) = Action { implicit request: Request[AnyContent] =>

        request.body.asJson match {
            case Some(body) =>
            val nameOpt = (body \ "name").asOpt[String]
            val priceOpt = (body \ "price").asOpt[Double]

            (nameOpt, priceOpt) match {
                case (Some(name), Some(price)) =>
                carts.find(_.id == cartId) match {
                    case Some(cart) =>
                    cart.productId += 1
                    val newProduct = Product(cart.productId, name, price)
                    cart.products += newProduct
                    Ok(s"Product added to Cart id=$cartId")

                    case None => NotFound(s"Cart with id=$cartId not found!")
                }

                case _ => BadRequest("Required fields are missing!")
            }

            case None => BadRequest("Request doesn't have a JSON body!")
        }

    }

}
