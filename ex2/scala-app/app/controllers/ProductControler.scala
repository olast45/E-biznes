package controllers

import javax.inject._
import play.api._
import play.api.libs.json._
import play.api.mvc._

import models.Product

@Singleton
class ProductController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {

    var products = scala.collection.mutable.ListBuffer.empty[Product]

    def showAll() = Action { implicit request: Request[AnyContent] => 

        if (products.isEmpty) {
            NotFound("There are no products to be displayed!")

        } else {

            val productsJS: JsArray = JsArray(
                products.map(product => Json.obj(
                    "id" -> product.id,
                    "name" -> product.name,
                    "price" -> product.price
                ))
            )
            
            Ok(productsJS)

        }
    }

    def showById(requestedId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundProduct = products.find(_.id == requestedId)

        foundProduct match {
            case Some(product) => Ok(Json.obj(
                "id" -> product.id,
                "name" -> product.name,
                "price" -> product.price
            ))
            case None => NotFound(s"Product with id=$requestedId not found!")
        }
    }


    def deleteProduct(requestedId: Long) = Action { implicit request: Request[AnyContent] =>

        val foundProduct = products.find(_.id == requestedId)

        foundProduct match {
            case Some(product) => 
                products -= product
                Ok(s"Product with id=$requestedId removed")

            case None => NotFound(s"Product with id=$requestedId not found!")
        }
    }

    def deleteAllProducts() = Action { implicit request: Request[AnyContent] =>

        if (products.isEmpty) {
            NotFound("There are no products to be deleted!")

        } else {

            products.clear()

            Ok("All products were deleted!")
        }
  
    }

    def updateProduct(requestedId: Long) = Action { implicit request: Request[AnyContent] =>

        request.body.asJson match {
            case Some(body) =>
                val nameOpt = (body \ "name").asOpt[String]
                val priceOpt = (body \ "price").asOpt[Double]

                val foundProduct = products.indexWhere(_.id == requestedId)
                foundProduct match {
                    case index if index >= 0 =>
                        val product = products(index)
                        val updatedProduct = product.copy(
                            name = nameOpt.getOrElse(product.name), 
                            price = priceOpt.getOrElse(product.price)
                        )

                        products.update(index, updatedProduct)

                        Ok(s"Product with id=$requestedId updated!")

                    case _ => NotFound(s"Product with id=$requestedId not found!")
                }

            case None => BadRequest("Request doesn't have a body!")
        }

    }

    def addProduct() = Action { implicit request: Request[AnyContent] =>
        request.body.asJson match {
            case Some(body) =>
                val idOpt = (body \ "id").asOpt[Long]
                val nameOpt = (body \ "name").asOpt[String]
                val priceOpt = (body \ "price").asOpt[Double]

                idOpt match {
                    case Some(id) => 
                        val foundProduct = products.find(_.id == id)
                        foundProduct match {
                            case Some(product) => Conflict(s"Product with id=$id already exists")

                            case None => 
                                if (nameOpt.isDefined && priceOpt.isDefined) {
                                    val newProduct = Product(id, nameOpt.get, priceOpt.get)
                                    products += newProduct
                                    Ok("Product added!")
                                } else {
                                    BadRequest("Required fields are missing!")
                                }
                        }

                    case None => BadRequest("Id field is missing!")    
                
                }

            case None => BadRequest("Request doesn't have a body!")
        }
    }
}
