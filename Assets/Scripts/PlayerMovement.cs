using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    [Header("References")]
    public CharacterController characterController;
    public Transform FPCamera; // VR camera / main camera

    [Header("Movement Settings")]
    public float speed = 5f;               // General movement speed
    public float rotationSpeed = 90f;      // Keyboard rotation speed
    public float gravity = -9.81f;         // Gravity
    public bool angleMove = true;          // Enable tilt forward movement

    [Header("Crouch Settings")]
    public bool allowCrouch = true;
    public float standingHeight = 2f;
    public float crouchHeight = 1f;
    
    private Vector3 velocity;
    private bool moveForward = false;
    private bool isGrounded;
    private bool isStanding = true;

    void Start()
    {
        if(characterController == null)
            characterController = GetComponent<CharacterController>();
    }

    void Update()
    {
        isGrounded = characterController.isGrounded;
        if(isGrounded && velocity.y < 0)
            velocity.y = 0f;

        // --- VR Tilt Forward Movement ---
        Vector3 tiltMove = Vector3.zero;
        if(angleMove && FPCamera != null)
        {
            float pitch = FPCamera.eulerAngles.x;
            if(pitch > 180) pitch -= 360; // Convert to -180 to 180

            if(pitch >= 30f) // toggleAngle
            {
                moveForward = true;
            }
            else
            {
                moveForward = false;
            }

            if(moveForward)
            {
                tiltMove = FPCamera.forward;
                tiltMove.y = 0f; // Keep horizontal
                tiltMove.Normalize();
            }
        }

        // --- Keyboard Input ---
        float x = Input.GetAxis("Horizontal");
        float z = Input.GetAxis("Vertical");

        Vector3 inputMove = transform.right * x + transform.forward * z;

        // Combine VR tilt + keyboard input
        Vector3 move = inputMove + tiltMove;
        if(move.magnitude > 1f) move.Normalize(); // Prevent faster diagonal speed
        characterController.Move(move * speed * Time.deltaTime);

        // --- Keyboard Rotation ---
        if(Mathf.Abs(x) > 0.1f)
        {
            float rotationAmount = x * rotationSpeed * Time.deltaTime;
            characterController.transform.Rotate(Vector3.up * rotationAmount);
        }

        // --- Gravity ---
        velocity.y += gravity * Time.deltaTime;
        characterController.Move(velocity * Time.deltaTime);

        // --- Crouch / Sit ---
        if(allowCrouch && Input.GetKeyDown(KeyCode.C))
        {
            if(isStanding)
            {
                characterController.height = crouchHeight;
                isStanding = false;
            }
            else
            {
                characterController.height = standingHeight;
                isStanding = true;
            }
        }
    }
}
